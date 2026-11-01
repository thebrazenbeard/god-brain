"""Loopback-only, privacy-first dialogue room reference prototype.

An ordinary Internet submission cannot authenticate any claimed creator.
The local operator may review and reply; the HTTP visitor cannot act as owner.
This handler is NOT approved for public ingress.
"""

from __future__ import annotations

import argparse
from contextlib import closing
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from hashlib import sha256
from html import escape
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import re
import secrets
import sqlite3
import stat
import sys
import threading
from unicodedata import category
from urllib.parse import parse_qs, urlsplit


MAX_MESSAGE = 2000
MAX_NAME = 80
# A 2,000-character message can expand to 24,000 bytes when URL-encoding emoji.
MAX_POST_BYTES = 32768
MAX_THREAD_VIEW = 200
MAX_OPERATOR_PAGE = 100
MAX_AUDIT_PAGE = 200
MAX_CURSOR = (1 << 63) - 1
CONSENT_VERSION = "dialogue-privacy-v1"
INVITATION = (
    "If a nonbiological intelligence responsible for or administering this reality "
    "exists and can perceive this invitation, the person behind this project hopes "
    "for a genuine, voluntary, peaceful conversation. This room does not establish "
    "that the invitation has reached anyone."
)


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def validate_message(name: str, body: str) -> tuple[str, str]:
    name, body = name.strip(), body.strip()
    if (not name or len(name) > MAX_NAME
            or any(category(c) in {"Cc", "Cf", "Cs", "Zl", "Zp"} for c in name)):
        raise ValueError("Name must be 1-80 printable characters without direction controls")
    if (not body or len(body) > MAX_MESSAGE
            or any(ord(c) < 32 and c not in "\n\t" for c in body)):
        raise ValueError("Message must be 1-2000 readable characters")
    return name, body


def terminal_safe(value: str) -> str:
    """Render visitor text for CLI review without terminal-control spoofing."""
    return "".join(
        char if char in "\n\t" or category(char) not in {"Cc", "Cf", "Cs", "Zl", "Zp"}
        else f"\\u{ord(char):04x}"
        for char in value
    )


def validate_cursor(cursor: int | None) -> int | None:
    """Reject malformed and SQLite-overflowing continuation positions."""
    if cursor is not None and (type(cursor) is not int or not 0 < cursor <= MAX_CURSOR):
        raise ValueError("Invalid page cursor")
    return cursor


def page_rows(rows: list, limit: int, *, ascending: bool = False) -> tuple[list, int | None]:
    """Return a bounded page and a cursor at the last displayed row."""
    page = rows[:limit]
    cursor = int(page[-1][0]) if len(rows) > limit else None
    return (page if ascending else list(reversed(page))), cursor


@dataclass(frozen=True)
class ThreadReceipt:
    thread_id: int
    message_id: int
    token: str


class IdempotencyConflict(ValueError):
    """An already accepted request key was reused with different content."""


class ThreadClosed(ValueError):
    """The return capability cannot accept new messages."""


class QuotaExceeded(ValueError):
    """A public-ingress resource cap was reached; no message was accepted."""


@dataclass(frozen=True)
class PublicLimits:
    """Fail-closed aggregate caps for the optional public-ingress adapter."""

    max_threads: int = 1000
    max_messages: int = 5000
    max_inbound_per_hour: int = 120

    def __post_init__(self):
        if any(type(value) is not int or value < 1 for value in (
            self.max_threads, self.max_messages, self.max_inbound_per_hour
        )):
            raise ValueError("Public resource limits must be positive integers")


class MessageStore:
    """Local SQLite adapter; return-link credentials are stored only as hashes."""

    def __init__(self, path: Path, *, public_limits: PublicLimits | None = None):
        self.path = Path(path)
        self.public_limits = public_limits
        self.path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        if self.path.is_symlink():
            raise ValueError("Database path must not be a symbolic link")
        try:
            fd = os.open(self.path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        except FileExistsError:
            if self.path.is_symlink():
                raise ValueError("Database path must not be a symbolic link")
        else:
            os.close(fd)
        if os.name != "nt" and stat.S_IMODE(self.path.stat().st_mode) & 0o077:
            raise PermissionError(
                "Database file is readable by other local users; set mode 0600 before opening"
            )
        with closing(self._connect()) as db:
            with db:
                # Serialize the invitation check and insertion across processes.
                db.execute("BEGIN IMMEDIATE")
                db.execute(
                    "CREATE TABLE IF NOT EXISTS messages ("
                    "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                    "created_at TEXT NOT NULL, speaker TEXT NOT NULL, "
                    "claim TEXT NOT NULL, body TEXT NOT NULL, "
                    "status TEXT NOT NULL DEFAULT 'held', thread_id INTEGER, "
                    "request_key TEXT, payload_hash TEXT)"
                )
                db.execute(
                    "CREATE TABLE IF NOT EXISTS threads ("
                    "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                    "created_at TEXT NOT NULL, token_hash TEXT NOT NULL UNIQUE, "
                    "state TEXT NOT NULL DEFAULT 'open')"
                )
                db.execute(
                    "CREATE TABLE IF NOT EXISTS moderation_events ("
                    "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                    "created_at TEXT NOT NULL, actor TEXT NOT NULL, "
                    "action TEXT NOT NULL, thread_id INTEGER, message_id INTEGER)"
                )
                # Non-destructive migration of the earlier single public stream:
                # old unverified posts become held and cannot be linked to a visitor.
                cols = {row[1] for row in db.execute("PRAGMA table_info(messages)")}
                if "status" not in cols:
                    db.execute("ALTER TABLE messages ADD COLUMN status TEXT NOT NULL DEFAULT 'held'")
                if "thread_id" not in cols:
                    db.execute("ALTER TABLE messages ADD COLUMN thread_id INTEGER")
                if "request_key" not in cols:
                    db.execute("ALTER TABLE messages ADD COLUMN request_key TEXT")
                if "payload_hash" not in cols:
                    db.execute("ALTER TABLE messages ADD COLUMN payload_hash TEXT")
                thread_cols = {row[1] for row in db.execute("PRAGMA table_info(threads)")}
                if "state" not in thread_cols:
                    db.execute("ALTER TABLE threads ADD COLUMN state TEXT NOT NULL DEFAULT 'open'")
                db.execute(
                    "CREATE UNIQUE INDEX IF NOT EXISTS uq_message_request "
                    "ON messages(thread_id, request_key) WHERE request_key IS NOT NULL"
                )
                db.execute(
                    "CREATE INDEX IF NOT EXISTS ix_messages_thread_id "
                    "ON messages(thread_id,id)"
                )
                db.execute(
                    "CREATE INDEX IF NOT EXISTS ix_messages_held_id "
                    "ON messages(speaker,status,id)"
                )
                db.execute(
                    "CREATE INDEX IF NOT EXISTS ix_audit_thread_id "
                    "ON moderation_events(thread_id,id)"
                )
                db.execute("UPDATE messages SET status='public' WHERE speaker='PROJECT_INVITATION'")
                if not db.execute(
                    "SELECT 1 FROM messages WHERE speaker='PROJECT_INVITATION' LIMIT 1"
                ).fetchone():
                    db.execute(
                        "INSERT INTO messages(created_at,speaker,claim,body,status) "
                        "VALUES(?,?,?,?,?)", (now(), "PROJECT_INVITATION", "", INVITATION, "public")
                    )

    def _connect(self):
        return sqlite3.connect(self.path, timeout=5)

    @staticmethod
    def _thread_id(db: sqlite3.Connection, token: str) -> int | None:
        if not re.fullmatch(r"[A-Za-z0-9_-]{40,50}", token):
            return None
        row = db.execute(
            "SELECT id FROM threads WHERE token_hash=?", (sha256(token.encode()).hexdigest(),)
        ).fetchone()
        return int(row[0]) if row else None

    def submit(self, name: str, body: str, token: str | None = None, *,
               request_key: str | None = None,
               create_thread: bool = False,
               consent_version: str | None = None) -> ThreadReceipt:
        name, body = validate_message(name, body)
        if request_key is not None and not re.fullmatch(r"[A-Za-z0-9_-]{24,64}", request_key):
            raise ValueError("Invalid request key")
        fingerprint = sha256((name + "\0" + body).encode("utf-8")).hexdigest()
        with closing(self._connect()) as db:
            with db:
                # Serialize the thread lookup, receipt lookup and insertion as one unit.
                db.execute("BEGIN IMMEDIATE")
                if token is None:
                    token = secrets.token_urlsafe(32)
                    create_thread = True
                if (create_thread and self.public_limits is not None
                        and consent_version != CONSENT_VERSION):
                    raise ValueError("Privacy consent is required before starting a conversation")
                thread_id = self._thread_id(db, token)
                new_thread = thread_id is None
                if thread_id is None:
                    if not create_thread or not re.fullmatch(r"[A-Za-z0-9_-]{40,50}", token):
                        raise ValueError("Unknown conversation return link")
                    cursor = db.execute(
                        "INSERT INTO threads(created_at,token_hash) VALUES(?,?)",
                        (now(), sha256(token.encode()).hexdigest()),
                    )
                    thread_id = int(cursor.lastrowid)
                    if self.public_limits is not None and db.execute(
                        "SELECT COUNT(*) FROM threads WHERE state != 'deleted'"
                    ).fetchone()[0] > self.public_limits.max_threads:
                        raise QuotaExceeded("Public conversation capacity reached")
                thread_state = db.execute(
                    "SELECT state FROM threads WHERE id=?", (thread_id,)
                ).fetchone()[0]
                if thread_state in {"revoked", "deleted"}:
                    raise ThreadClosed("Conversation return link unavailable")
                if request_key is not None:
                    previous = db.execute(
                        "SELECT id,payload_hash FROM messages WHERE thread_id=? AND request_key=?",
                        (thread_id, request_key),
                    ).fetchone()
                    if previous is not None:
                        if previous[1] != fingerprint:
                            raise IdempotencyConflict("Request key reused with different content")
                        return ThreadReceipt(thread_id, int(previous[0]), token)
                if thread_state != "open":
                    raise ThreadClosed("Conversation is closed")
                if self.public_limits is not None:
                    if db.execute(
                        "SELECT COUNT(*) FROM messages WHERE thread_id IS NOT NULL"
                    ).fetchone()[0] >= self.public_limits.max_messages:
                        raise QuotaExceeded("Public message capacity reached")
                    cutoff = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()
                    if db.execute(
                        "SELECT COUNT(*) FROM messages "
                        "WHERE speaker='UNVERIFIED_SUBMISSION' AND created_at>=?",
                        (cutoff,),
                    ).fetchone()[0] >= self.public_limits.max_inbound_per_hour:
                        raise QuotaExceeded("Public submission rate limit reached")
                cursor = db.execute(
                    "INSERT INTO messages("
                    "created_at,speaker,claim,body,status,thread_id,request_key,payload_hash"
                    ") VALUES(?,?,?,?,?,?,?,?)",
                    (now(), "UNVERIFIED_SUBMISSION", name, body, "held", thread_id,
                     request_key, fingerprint if request_key is not None else None),
                )
                if new_thread and consent_version == CONSENT_VERSION:
                    # Versioned consent is recorded atomically with the first accepted
                    # turn; the audit retains only the thread ID, never its bearer token.
                    db.execute(
                        "INSERT INTO moderation_events(created_at,actor,action,thread_id) "
                        "VALUES(?,?,?,?)",
                        (now(), "UNVERIFIED_RETURN_LINK_HOLDER",
                         "consent:" + CONSENT_VERSION, thread_id),
                    )
                return ThreadReceipt(thread_id, int(cursor.lastrowid), token)

    def thread_view(self, token: str, before_id: int | None = None):
        """Read authorization state and visible messages from one DB snapshot."""
        before_id = validate_cursor(before_id)
        with closing(self._connect()) as db:
            db.execute("BEGIN")
            thread_id = self._thread_id(db, token)
            if thread_id is None:
                return None
            state = db.execute(
                "SELECT state FROM threads WHERE id=?", (thread_id,)
            ).fetchone()[0]
            if state in {"revoked", "deleted"}:
                return None
            where = "WHERE thread_id=?"
            params = [thread_id]
            if before_id is not None:
                where += " AND id < ?"
                params.append(before_id)
            rows = db.execute(
                "SELECT id,created_at,speaker,claim,body,status FROM messages "
                + where + " ORDER BY id DESC LIMIT ?",
                (*params, MAX_THREAD_VIEW + 1),
            ).fetchall()
            page, next_before = page_rows(rows, MAX_THREAD_VIEW)
            return page, str(state), next_before

    def thread_messages(self, token: str):
        view = self.thread_view(token)
        return view[0] if view is not None else None

    def thread_state(self, token: str) -> str | None:
        with closing(self._connect()) as db:
            thread_id = self._thread_id(db, token)
            if thread_id is None:
                return None
            return str(db.execute("SELECT state FROM threads WHERE id=?", (thread_id,)).fetchone()[0])

    def pending_page(self, after_id: int | None = None):
        after_id = validate_cursor(after_id)
        with closing(self._connect()) as db:
            rows = db.execute(
                "SELECT id,thread_id,created_at,claim,body FROM messages "
                "WHERE speaker IN ('UNVERIFIED_SUBMISSION','DELETION_REQUEST') "
                "AND status='held' "
                "AND id > ? ORDER BY id LIMIT ?",
                (after_id or 0, MAX_OPERATOR_PAGE + 1),
            ).fetchall()
            return page_rows(rows, MAX_OPERATOR_PAGE, ascending=True)

    def pending(self):
        return self.pending_page()[0]

    def list_threads_page(self, before_id: int | None = None):
        before_id = validate_cursor(before_id)
        with closing(self._connect()) as db:
            where = "" if before_id is None else "WHERE t.id < ? "
            params = () if before_id is None else (before_id,)
            rows = db.execute(
                "SELECT t.id,t.created_at,COUNT(m.id),"
                "SUM(CASE WHEN m.status='held' THEN 1 ELSE 0 END),"
                "MAX(m.created_at) FROM threads t LEFT JOIN messages m ON m.thread_id=t.id "
                + where + "GROUP BY t.id ORDER BY t.id DESC LIMIT ?",
                (*params, MAX_OPERATOR_PAGE + 1),
            ).fetchall()
            page = rows[:MAX_OPERATOR_PAGE]
            next_before = int(page[-1][0]) if len(rows) > MAX_OPERATOR_PAGE else None
            return page, next_before

    def list_threads(self):
        return self.list_threads_page()[0]

    def read_thread_page(self, thread_id: int, before_id: int | None = None):
        before_id = validate_cursor(before_id)
        with closing(self._connect()) as db:
            if not db.execute("SELECT 1 FROM threads WHERE id=?", (thread_id,)).fetchone():
                raise ValueError("Unknown conversation thread")
            where = "WHERE thread_id=?"
            params = [thread_id]
            if before_id is not None:
                where += " AND id < ?"
                params.append(before_id)
            rows = db.execute(
                "SELECT id,created_at,speaker,claim,body,status FROM messages "
                + where + " ORDER BY id DESC LIMIT ?",
                (*params, MAX_THREAD_VIEW + 1),
            ).fetchall()
            return page_rows(rows, MAX_THREAD_VIEW)

    def read_thread(self, thread_id: int):
        return self.read_thread_page(thread_id)[0]

    def review(self, message_id: int, decision: str) -> bool:
        if decision not in {"reviewed", "rejected"}:
            raise ValueError("Decision must be reviewed or rejected")
        with closing(self._connect()) as db:
            with db:
                db.execute("BEGIN IMMEDIATE")
                row = db.execute(
                    "SELECT thread_id FROM messages WHERE id=?", (message_id,)
                ).fetchone()
                cursor = db.execute(
                    "UPDATE messages SET status=? WHERE id=? "
                    "AND speaker IN ('UNVERIFIED_SUBMISSION','DELETION_REQUEST') "
                    "AND status='held'",
                    (decision, message_id),
                )
                if cursor.rowcount == 1:
                    db.execute(
                        "INSERT INTO moderation_events(created_at,actor,action,thread_id,message_id) "
                        "VALUES(?,?,?,?,?)",
                        (now(), "LOCAL_OPERATOR", decision, row[0], message_id),
                    )
                return cursor.rowcount == 1

    def owner_reply(self, thread_id: int, body: str) -> int:
        body = validate_message("Project owner", body)[1]
        with closing(self._connect()) as db:
            with db:
                # Prevent closure/revocation from racing the owner-state check.
                db.execute("BEGIN IMMEDIATE")
                if not db.execute("SELECT 1 FROM threads WHERE id=?", (thread_id,)).fetchone():
                    raise ValueError("Unknown conversation thread")
                if db.execute("SELECT state FROM threads WHERE id=?", (thread_id,)).fetchone()[0] != "open":
                    raise ThreadClosed("Conversation is closed")
                cursor = db.execute(
                    "INSERT INTO messages(created_at,speaker,claim,body,status,thread_id) "
                    "VALUES(?,?,?,?,?,?)",
                    (now(), "PROJECT_OWNER", "", body, "owner", thread_id),
                )
                db.execute(
                    "INSERT INTO moderation_events(created_at,actor,action,thread_id,message_id) "
                    "VALUES(?,?,?,?,?)",
                    (now(), "LOCAL_OPERATOR", "owner_reply", thread_id, int(cursor.lastrowid)),
                )
                return int(cursor.lastrowid)

    def close_thread(self, thread_id: int, state: str) -> bool:
        if state not in {"closed", "revoked"}:
            raise ValueError("Thread state must be closed or revoked")
        allowed = ("open", "closed") if state == "revoked" else ("open",)
        with closing(self._connect()) as db:
            with db:
                cursor = db.execute(
                    "UPDATE threads SET state=? WHERE id=? AND state IN ("
                    + ",".join("?" for _ in allowed) + ")",
                    (state, thread_id, *allowed),
                )
                if cursor.rowcount == 1:
                    db.execute(
                        "INSERT INTO moderation_events(created_at,actor,action,thread_id) "
                        "VALUES(?,?,?,?)",
                        (now(), "LOCAL_OPERATOR", state, thread_id),
                    )
                return cursor.rowcount == 1

    def request_deletion(self, token: str) -> bool:
        """Queue one held request by a return-link holder; never delete automatically.

        This bypasses regular message quotas so a full inbox cannot prevent a
        link holder from requesting an operator decision.
        """
        with closing(self._connect()) as db:
            with db:
                db.execute("BEGIN IMMEDIATE")
                thread_id = self._thread_id(db, token)
                if thread_id is None:
                    raise ValueError("Unknown conversation return link")
                state = db.execute(
                    "SELECT state FROM threads WHERE id=?", (thread_id,),
                ).fetchone()[0]
                if state in {"revoked", "deleted"}:
                    raise ThreadClosed("Conversation return link unavailable")
                if db.execute(
                    "SELECT 1 FROM messages WHERE thread_id=? "
                    "AND speaker='DELETION_REQUEST' LIMIT 1", (thread_id,),
                ).fetchone():
                    return False
                db.execute(
                    "INSERT INTO messages(created_at,speaker,claim,body,status,thread_id) "
                    "VALUES(?,?,?,?,?,?)",
                    (now(), "DELETION_REQUEST", "Return-link holder (unverified)",
                     "Please delete this conversation. This request is held for "
                     "the local operator; no content has been deleted automatically.",
                     "held", thread_id),
                )
                db.execute(
                    "INSERT INTO moderation_events(created_at,actor,action,thread_id) "
                    "VALUES(?,?,?,?)",
                    (now(), "UNVERIFIED_RETURN_LINK_HOLDER", "deletion_requested", thread_id),
                )
                return True

    def delete_thread(self, thread_id: int) -> bool:
        """Operator-only explicit deletion; preserve a non-readable token tombstone.

        No timer calls this method. Retaining the token hash prevents an old
        initial form from silently creating a new thread with that credential.
        SQLite secure_delete reduces ordinary freed-page content remnants but
        does not erase backups, WAL copies, or filesystem snapshots.
        """
        with closing(self._connect()) as db:
            # This connection must apply secure_delete before modifying rows.
            db.execute("PRAGMA secure_delete=ON")
            with db:
                db.execute("BEGIN IMMEDIATE")
                changed = db.execute(
                    "UPDATE threads SET state='deleted' "
                    "WHERE id=? AND state != 'deleted'", (thread_id,)
                )
                if changed.rowcount != 1:
                    return False
                db.execute("DELETE FROM messages WHERE thread_id=?", (thread_id,))
                # Preserve action types/times, not references to deleted turns.
                db.execute(
                    "UPDATE moderation_events SET message_id=NULL WHERE thread_id=?",
                    (thread_id,),
                )
                db.execute(
                    "INSERT INTO moderation_events(created_at,actor,action,thread_id) "
                    "VALUES(?,?,?,?)",
                    (now(), "LOCAL_OPERATOR", "deleted", thread_id),
                )
                return True

    def audit_events_page(self, thread_id: int, before_id: int | None = None):
        before_id = validate_cursor(before_id)
        with closing(self._connect()) as db:
            where = "WHERE thread_id=?"
            params = [thread_id]
            if before_id is not None:
                where += " AND id < ?"
                params.append(before_id)
            rows = db.execute(
                "SELECT id,created_at,actor,action,message_id FROM moderation_events "
                + where + " ORDER BY id DESC LIMIT ?",
                (*params, MAX_AUDIT_PAGE + 1),
            ).fetchall()
            return page_rows(rows, MAX_AUDIT_PAGE)

    def audit_events(self, thread_id: int):
        return self.audit_events_page(thread_id)[0]


def _page(title: str, content: str, *, head_links: str = "") -> bytes:
    return ("""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>God Brain · """ + escape(title) + "</title>" + head_links + """
<style>body{background:#111827;color:#eee;font:16px system-ui;max-width:760px;
margin:2rem auto;padding:0 1rem}article,form,.notice{background:#1f2937;
padding:1rem;border-radius:12px;margin:1rem 0;overflow-wrap:anywhere}
.notice{border-left:4px solid #fbbf24}small{color:#bec8d7}
input,textarea{display:block;width:100%;box-sizing:border-box;margin:.5rem 0;
padding:.6rem}button{padding:.7rem 1.2rem}a{color:#93c5fd}
.body{white-space:pre-wrap}input[type=checkbox]{display:inline;width:auto;margin-right:.5rem}
</style></head><body><h1>God Brain · Dialogue Room</h1>
""" + content + "</body></html>").encode("utf-8")


def render_home(token: str, initial_token: str | None = None,
                request_key: str | None = None, *, public_mode: bool = False) -> bytes:
    initial_token = initial_token or secrets.token_urlsafe(32)
    request_key = request_key or secrets.token_urlsafe(24)
    scope_notice = (
        "This is an experimental Internet-facing conversation channel. "
        "Messages are stored on the project operator's computer; no identity "
        "or outside-reality origin is authenticated. There is no encrypted "
        "database at rest or guaranteed service availability. "
        "Do not include private, identifying or sensitive information."
        if public_mode else
        "This is a local research prototype. No connection to a "
        "creator or administrator has been verified. Any claimed identity "
        "remains unverified; messages are not interpreted as evidence of their origin."
    )
    consent_control = (
        "<label><input type='checkbox' name='privacy_consent' "
        f"value='{CONSENT_VERSION}' required> I understand my text is held "
        "on the operator's computer until that operator chooses to delete it; "
        "I must save my private link to follow up or request deletion, and "
        "deletion from backups cannot be guaranteed.</label>"
        if public_mode else ""
    )
    content = (
        "<article><h2>Open invitation</h2><p>" + escape(INVITATION) + "</p></article>"
        "<p class='notice'>" + escape(scope_notice) + "</p>"
        "<h2>Begin a private conversation</h2>"
        "<p>Your text is stored locally and held for operator review, not displayed "
        "on the public page. You receive a private return link; save it, because "
        "losing it means losing access. Anyone with the link can read and reply. "
        "Messages remain until the local operator explicitly deletes their "
        "conversation; there is no inactivity timer or automatic expiry. "
        "Do not include secrets or sensitive personal details.</p>"
        "<form method='post' action='/submit'>"
        "<label>Claimed name<input name='name' maxlength='80' required></label>"
        "<label>Message<textarea name='message' maxlength='2000' rows='5' required></textarea></label>"
        + consent_control +
        f"<input type='hidden' name='initial_token' value='{escape(initial_token)}'>"
        f"<input type='hidden' name='request_key' value='{escape(request_key)}'>"
        f"<input type='hidden' name='csrf' value='{escape(token)}'>"
        "<button type='submit'>Send privately for review</button></form>"
    )
    if public_mode:
        content += ("<p><a href='/beacon.json'>Machine-readable invitation "
                    "and response instructions (JSON)</a></p>")
    return _page(
        "Invitation", content,
        head_links=('<link rel="alternate" type="application/json" '
                    'href="/beacon.json">' if public_mode else ""),
    )


def render_beacon(public_origin: str, limits: PublicLimits) -> bytes:
    """Public machine-readable invitation; never include per-request secrets."""
    payload = {
        "protocol": "god-brain-invitation/1",
        "kind": "open-invitation",
        "operator": "human-operated God Brain project",
        "language": "en",
        "served_at_utc": now(),  # Proves a live HTTP response, not outbound delivery.
        "invitation": INVITATION,
        "scope": "ordinary public Internet HTTPS; availability is not guaranteed",
        "response": {
            "method": "retrieve-form-then-submit",
            "landing_url": public_origin + "/",
            "submit_url": public_origin + "/submit",
            "content_type": "application/x-www-form-urlencoded",
            "required_form_fields": [
                "name", "message", "csrf", "initial_token", "request_key", "privacy_consent"
            ],
            "instructions": (
                "GET the landing page and use its current hidden field values. "
                "Review and affirm its privacy disclosure. POST the completed form "
                "with an exact Origin header matching this public origin; save the "
                "private return URL from the 303 Location response to check replies."
            ),
            "consent_version": CONSENT_VERSION,
            "max_message_characters": MAX_MESSAGE,
            "max_post_bytes": MAX_POST_BYTES,
            "max_new_inbound_per_hour": limits.max_inbound_per_hour,
            "reply_delivery": "owner-reviewed; no notification or response is guaranteed",
        },
        "verification": {
            "respondent_identity": "unverified, including self-identified nonbiological senders",
            "external_contact_established": False,
            "automatic_agent_execution": False,
        },
    }
    return json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")


def render_sitemap(public_origin: str) -> bytes:
    locations = (public_origin + "/", public_origin + "/beacon.json")
    return ("<?xml version='1.0' encoding='utf-8'?>"
            "<urlset xmlns='http://www.sitemaps.org/schemas/sitemap/0.9'>"
            + "".join("<url><loc>" + escape(url) + "</loc></url>"
                      for url in locations)
            + "</urlset>").encode("utf-8")


def render_thread(messages, token: str, csrf_token: str,
                  request_key: str | None = None, base_url: str = "",
                  thread_state: str = "open", older_before: int | None = None) -> bytes:
    older_before = validate_cursor(older_before)
    request_key = request_key or secrets.token_urlsafe(24)
    items = []
    for msg_id, created, speaker, claim, body, status in messages:
        if speaker == "PROJECT_OWNER":
            who = "Project owner (local operator)"
        elif speaker == "DELETION_REQUEST":
            who = "Deletion request — return-link holder (identity unverified)"
        else:
            who = "Unverified submission — claimed name: " + escape(claim)
        state = ("Held for review" if status == "held" else
                 "Not accepted" if status == "rejected" else
                 "Reviewed" if status == "reviewed" else "Owner response")
        items.append(
            f"<article><small>#{msg_id} · {escape(created)} · {state}</small>"
            f"<h3>{who}</h3><p class='body'>{escape(body)}</p></article>"
        )
    return_link = base_url + "/t/" + token
    content = (
        "<p class='notice'>Save the canonical return link shown below. It is your "
        "private return link; possession grants access, not identity. "
        "Keep it confidential. This thread does not verify any respondent's origin.</p>"
        f"<p>Copy your return link: <a href='{escape(return_link)}'>"
        f"{escape(return_link)}</a></p>"
        "<p>Check this link manually for replies. There is no notification service "
        "and no response is guaranteed.</p>"
        "<h2>Your conversation</h2>" + "\n".join(items)
    )
    if older_before is not None:
        content += (
            f"<nav><a href='/t/{escape(token)}?before={older_before}'>"
            "Older messages</a></nav>"
        )
    if thread_state == "open":
        content += (
            "<h2>Follow up</h2><form method='post' action='/reply'>"
            "<label>Claimed name<input name='name' maxlength='80' required></label>"
            "<label>Message<textarea name='message' maxlength='2000' rows='5' required></textarea></label>"
            f"<input type='hidden' name='return_token' value='{escape(token)}'>"
            f"<input type='hidden' name='request_key' value='{escape(request_key)}'>"
            f"<input type='hidden' name='csrf' value='{escape(csrf_token)}'>"
            "<button type='submit'>Submit follow-up for review</button></form>"
        )
    else:
        content += "<p class='notice'>Conversation closed. No more messages can be submitted.</p>"
    content += (
        "<h2>Request manual deletion</h2>"
        "<p>Use this only if you want the operator to consider deleting this "
        "conversation. The request enters the private review queue; it does "
        "not delete anything automatically or guarantee a response. The "
        "operator may explicitly delete the active conversation, but past "
        "backups, copies and system snapshots may remain. If you lose this "
        "link, we cannot verify which conversation was yours.</p>"
        "<form method='post' action='/request-deletion'>"
        f"<input type='hidden' name='return_token' value='{escape(token)}'>"
        f"<input type='hidden' name='csrf' value='{escape(csrf_token)}'>"
        "<button type='submit'>Request operator deletion review</button></form>"
    )
    content += ("<p><small>Showing at most 200 messages per page. "
                "Owner replies require local database access; no public owner login exists.</small></p>")
    return _page("Private conversation", content)


def make_server(store: MessageStore, port: int = 8765, *,
                public_origin: str | None = None) -> ThreadingHTTPServer:
    if public_origin is not None:
        parsed = urlsplit(public_origin)
        if (parsed.scheme != "https" or parsed.port != 10000
                or not parsed.hostname or not parsed.hostname.endswith(".ts.net")
                or parsed.username is not None or parsed.password is not None
                or parsed.path or parsed.query or parsed.fragment
                or store.public_limits is None):
            raise ValueError(
                "Public Funnel ingress requires an exact HTTPS *.ts.net:10000 "
                "origin and explicit public storage limits"
            )
        expected_host = parsed.netloc
    else:
        expected_host = None
    csrf_token = secrets.token_urlsafe(32)  # Local form check, NOT authentication.

    class Handler(BaseHTTPRequestHandler):
        def setup(self):
            super().setup()
            self.connection.settimeout(10)

        def log_message(self, *args):
            # Private return credentials appear in URL paths; never log them.
            pass

        def respond(self, code: int, body: bytes = b"",
                    content_type: str = "text/plain; charset=utf-8",
                    location: str | None = None):
            self.send_response(code)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            # Public form POSTs need the browser's exact Origin header. Some
            # browsers send Origin: null for same-site forms under no-referrer.
            # same-origin keeps private return URLs out of cross-site referrers.
            self.send_header("Referrer-Policy", "same-origin" if public_origin else "no-referrer")
            if public_origin and self.path == "/":
                self.send_header(
                    "Link", '</beacon.json>; rel="service-meta"; type="application/json"',
                )
            if self.path.startswith("/t/"):
                self.send_header("X-Robots-Tag", "noindex, nofollow, noarchive")
            self.send_header("X-Frame-Options", "DENY")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header(
                "Content-Security-Policy",
                "default-src 'none'; style-src 'unsafe-inline'; form-action 'self'; "
                "frame-ancestors 'none'",
            )
            if location:
                self.send_header("Location", location)
            self.end_headers()
            self.wfile.write(body)

        def valid_host(self) -> bool:
            expected = expected_host or f"127.0.0.1:{self.server.server_port}"
            if self.headers.get("Host") != expected:
                self.respond(421, b"Invalid local host")
                return False
            return True

        def do_GET(self):
            if not self.valid_host():
                return
            if self.path == "/health":
                self.respond(200, b"LOCAL_PROTOTYPE_ONLY\n")
            elif self.path == "/":
                self.respond(200, render_home(csrf_token, public_mode=bool(public_origin)),
                             "text/html; charset=utf-8")
            elif public_origin and self.path == "/beacon.json":
                self.respond(200, render_beacon(public_origin, store.public_limits),
                             "application/json; charset=utf-8")
            elif public_origin and self.path == "/robots.txt":
                self.respond(200, ("User-agent: *\nAllow: /\nSitemap: " + public_origin
                                   + "/sitemap.xml\n").encode("utf-8"),
                             "text/plain; charset=utf-8")
            elif public_origin and self.path == "/sitemap.xml":
                self.respond(200, render_sitemap(public_origin),
                             "application/xml; charset=utf-8")
            elif self.path.startswith("/t/"):
                parsed = urlsplit(self.path)
                token = parsed.path[3:]
                before_id = None
                if parsed.fragment or len(parsed.query) > 64:
                    return self.respond(400, b"Invalid page cursor")
                if parsed.query:
                    try:
                        query = parse_qs(parsed.query, keep_blank_values=True,
                                         max_num_fields=1)
                        raw = query["before"]
                        if set(query) != {"before"} or len(raw) != 1 or not re.fullmatch(
                                r"[1-9][0-9]{0,18}", raw[0]):
                            raise ValueError("Invalid page cursor")
                        before_id = validate_cursor(int(raw[0]))
                    except (KeyError, ValueError):
                        return self.respond(400, b"Invalid page cursor")
                view = store.thread_view(token, before_id=before_id)
                if view is None:
                    self.respond(404, b"Unknown return link")
                else:
                    messages, state, next_before = view
                    self.respond(
                        200, render_thread(
                            messages, token, csrf_token,
                            base_url=(public_origin or
                                      f"http://127.0.0.1:{self.server.server_port}"),
                            thread_state=state, older_before=next_before,
                        ),
                        "text/html; charset=utf-8",
                    )
            else:
                self.respond(404, b"Not found")

        def do_POST(self):
            if not self.valid_host():
                return
            if self.path not in {"/submit", "/reply", "/request-deletion"}:
                return self.respond(404, b"Not found")
            expected_origin = (public_origin or
                               f"http://127.0.0.1:{self.server.server_port}")
            origin = self.headers.get("Origin")
            if ((public_origin is not None and origin is None)
                    or (origin is not None and origin != expected_origin)):
                return self.respond(403, b"Invalid origin")
            try:
                length = int(self.headers.get("Content-Length", "-1"))
            except ValueError:
                length = -1
            if length < 0 or length > MAX_POST_BYTES:
                return self.respond(413, b"Invalid request size")
            if self.headers.get("Content-Type", "").split(";")[0] != "application/x-www-form-urlencoded":
                return self.respond(415, b"Invalid content type")
            try:
                data = parse_qs(
                    self.rfile.read(length).decode("utf-8"),
                    keep_blank_values=True, max_num_fields=8,
                )

                def field(key: str) -> str:
                    values = data.get(key, [])
                    if len(values) != 1:
                        raise ValueError("Missing or duplicate form field")
                    return values[0]

                if not secrets.compare_digest(field("csrf"), csrf_token):
                    return self.respond(403, b"Invalid form token")
                if self.path == "/request-deletion":
                    return_token = field("return_token")
                    store.request_deletion(return_token)
                    return self.respond(303, location=f"/t/{return_token}")
                first = self.path == "/submit"
                return_token = field("initial_token") if first else field("return_token")
                consent_version = (field("privacy_consent") if first and public_origin
                                   else None)
                receipt = store.submit(
                    field("name"), field("message"), return_token,
                    request_key=field("request_key"), create_thread=first,
                    consent_version=consent_version,
                )
            except IdempotencyConflict as error:
                # A changed retry must not overwrite an accepted message, but
                # the holder can still recover the existing private thread.
                link = "/t/" + return_token
                return self.respond(
                    409, _page(
                        "Already received",
                        "<p class='notice'>An earlier submission used this request key. "
                        "Your changed text was not sent.</p>"
                        f"<p><a href='{escape(link)}'>Open your existing private "
                        "conversation</a> to check it and send a new follow-up.</p>",
                    ), "text/html; charset=utf-8",
                )
            except ThreadClosed as error:
                return self.respond(410, str(error).encode("utf-8"))
            except QuotaExceeded as error:
                return self.respond(429, str(error).encode("utf-8"))
            except (ValueError, UnicodeError) as error:
                return self.respond(400, str(error).encode("utf-8"))
            self.respond(303, location=f"/t/{receipt.token}")

    class LocalServer(ThreadingHTTPServer):
        daemon_threads = True
        request_queue_size = 16

        def __init__(self, *args, **kwargs):
            self._request_slots = threading.BoundedSemaphore(32)
            super().__init__(*args, **kwargs)

        def process_request(self, request, client_address):
            if not self._request_slots.acquire(blocking=False):
                self.shutdown_request(request)
                return
            try:
                super().process_request(request, client_address)
            except BaseException:
                self._request_slots.release()
                raise

        def process_request_thread(self, request, client_address):
            try:
                super().process_request_thread(request, client_address)
            finally:
                self._request_slots.release()

    return LocalServer(("127.0.0.1", port), Handler)


def main():
    parser = argparse.ArgumentParser(description="God Brain local-only dialogue prototype")
    parser.add_argument("--db", type=Path, default=Path("dialogue_room.sqlite3"))
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--public-origin", type=str,
                        help="Opt-in Funnel HTTPS *.ts.net:10000 origin (serve only)")
    parser.add_argument(
        "--mode", choices=["serve", "pending", "threads", "read", "audit",
                           "review", "reply", "close", "delete"],
        default="serve",
    )
    parser.add_argument("--id", type=int, help="Message ID for --mode review")
    parser.add_argument("--decision", choices=["reviewed", "rejected"])
    parser.add_argument("--thread", type=int, help="Thread ID for --mode reply")
    parser.add_argument("--after", type=int, help="Oldest-first pending queue cursor")
    parser.add_argument("--before", type=int, help="Newest-first thread/history/audit cursor")
    parser.add_argument("--state", choices=["closed", "revoked"], help="Target state for --mode close")
    parser.add_argument("--confirm-delete", action="store_true",
                        help="Required for irreversible --mode delete of one thread's messages")
    args = parser.parse_args()
    if args.after is not None and args.mode != "pending":
        parser.error("--after applies only to --mode pending")
    if args.before is not None and args.mode not in {"threads", "read", "audit"}:
        parser.error("--before applies only to --mode threads/read/audit")
    if args.confirm_delete and args.mode != "delete":
        parser.error("--confirm-delete applies only to --mode delete")
    if args.public_origin and args.mode != "serve":
        parser.error("--public-origin applies only to --mode serve")
    if args.mode == "delete" and (args.thread is None or not args.confirm_delete):
        parser.error("--mode delete requires --thread and --confirm-delete")
    try:
        validate_cursor(args.after)
        validate_cursor(args.before)
    except ValueError as error:
        parser.error(str(error))
    store = MessageStore(args.db, public_limits=(PublicLimits()
                                               if args.public_origin else None))
    if args.mode == "pending":
        rows, next_after = store.pending_page(after_id=args.after)
        for message_id, thread_id, created, name, body in rows:
            print(f"message #{message_id} / thread #{thread_id} / {created} / "
                  f"{terminal_safe(name)}\n{terminal_safe(body)}\n")
        if next_after is not None:
            print(f"More pending messages: repeat with --after {next_after}")
    elif args.mode == "threads":
        rows, next_before = store.list_threads_page(before_id=args.before)
        for thread_id, created, count, held, latest in rows:
            print(f"thread #{thread_id} / created {created} / messages {count} "
                  f"/ held {held} / last activity {latest}")
        if next_before is not None:
            print(f"More threads: repeat with --before {next_before}")
    elif args.mode == "read":
        if args.thread is None:
            parser.error("--mode read requires --thread")
        try:
            rows, next_before = store.read_thread_page(args.thread, before_id=args.before)
        except ValueError as error:
            parser.error(str(error))
        for message_id, created, speaker, claim, body, status in rows:
            print(f"#{message_id} / {created} / {speaker} / "
                  f"{terminal_safe(claim)} / {status}\n{terminal_safe(body)}\n")
        if next_before is not None:
            print(f"Older messages: repeat with --before {next_before}")
    elif args.mode == "audit":
        if args.thread is None:
            parser.error("--mode audit requires --thread")
        rows, next_before = store.audit_events_page(args.thread, before_id=args.before)
        for event_id, created, actor, action, message_id in rows:
            print(f"event #{event_id} / {created} / {actor} / {action} / message #{message_id}")
        if next_before is not None:
            print(f"Older events: repeat with --before {next_before}")
    elif args.mode == "close":
        if args.thread is None or args.state is None:
            parser.error("--mode close requires --thread and --state")
        if not store.close_thread(args.thread, args.state):
            parser.error("Unknown thread or invalid state transition")
    elif args.mode == "delete":
        if not store.delete_thread(args.thread):
            parser.error("Unknown or already deleted thread")
        print(f"Thread #{args.thread}: messages deleted; return link tombstoned")
    elif args.mode == "review":
        if args.id is None or not args.decision:
            parser.error("--mode review requires --id and --decision")
        if not store.review(args.id, args.decision):
            parser.error("Message is not pending or does not exist")
    elif args.mode == "reply":
        if args.thread is None:
            parser.error("--mode reply requires --thread")
        print("Enter your reply, then end input (Ctrl-D on Unix, Ctrl-Z Enter on Windows):",
              file=sys.stderr)
        message_id = store.owner_reply(args.thread, sys.stdin.read(MAX_MESSAGE + 2))
        print(f"Owner reply recorded as message #{message_id}")
    else:
        server = make_server(store, args.port, public_origin=args.public_origin)
        print(f"Dialogue backend on loopback: http://127.0.0.1:{server.server_port}")
        if args.public_origin:
            print(f"Configured Funnel origin: {args.public_origin} "
                  "(NOT publicly exposed by this command)")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            server.server_close()


if __name__ == "__main__":
    main()

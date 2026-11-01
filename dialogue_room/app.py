"""Loopback-only, privacy-first dialogue room reference prototype.

An ordinary Internet submission cannot authenticate any claimed creator.
The local operator may review and reply; the HTTP visitor cannot act as owner.
This handler is NOT approved for public ingress.
"""

from __future__ import annotations

import argparse
from contextlib import closing
from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
from html import escape
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import os
from pathlib import Path
import re
import secrets
import sqlite3
import stat
import sys
from unicodedata import category
from urllib.parse import parse_qs


MAX_MESSAGE = 2000
MAX_NAME = 80
MAX_POST_BYTES = 4096
MAX_THREAD_VIEW = 200
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


@dataclass(frozen=True)
class ThreadReceipt:
    thread_id: int
    message_id: int
    token: str


class MessageStore:
    """Local SQLite adapter; return-link credentials are stored only as hashes."""

    def __init__(self, path: Path):
        self.path = Path(path)
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
                    "status TEXT NOT NULL DEFAULT 'held', thread_id INTEGER)"
                )
                db.execute(
                    "CREATE TABLE IF NOT EXISTS threads ("
                    "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                    "created_at TEXT NOT NULL, token_hash TEXT NOT NULL UNIQUE)"
                )
                # Non-destructive migration of the earlier single public stream:
                # old unverified posts become held and cannot be linked to a visitor.
                cols = {row[1] for row in db.execute("PRAGMA table_info(messages)")}
                if "status" not in cols:
                    db.execute("ALTER TABLE messages ADD COLUMN status TEXT NOT NULL DEFAULT 'held'")
                if "thread_id" not in cols:
                    db.execute("ALTER TABLE messages ADD COLUMN thread_id INTEGER")
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

    def submit(self, name: str, body: str, token: str | None = None) -> ThreadReceipt:
        name, body = validate_message(name, body)
        with closing(self._connect()) as db:
            with db:
                if token is None:
                    token = secrets.token_urlsafe(32)
                    cursor = db.execute(
                        "INSERT INTO threads(created_at,token_hash) VALUES(?,?)",
                        (now(), sha256(token.encode()).hexdigest()),
                    )
                    thread_id = int(cursor.lastrowid)
                else:
                    thread_id = self._thread_id(db, token)
                    if thread_id is None:
                        raise ValueError("Unknown conversation return link")
                cursor = db.execute(
                    "INSERT INTO messages(created_at,speaker,claim,body,status,thread_id) "
                    "VALUES(?,?,?,?,?,?)",
                    (now(), "UNVERIFIED_SUBMISSION", name, body, "held", thread_id),
                )
                return ThreadReceipt(thread_id, int(cursor.lastrowid), token)

    def thread_messages(self, token: str):
        with closing(self._connect()) as db:
            thread_id = self._thread_id(db, token)
            if thread_id is None:
                return None
            rows = db.execute(
                "SELECT id,created_at,speaker,claim,body,status FROM messages "
                "WHERE thread_id=? ORDER BY id DESC LIMIT ?",
                (thread_id, MAX_THREAD_VIEW),
            ).fetchall()
            return list(reversed(rows))

    def pending(self):
        with closing(self._connect()) as db:
            return db.execute(
                "SELECT id,thread_id,created_at,claim,body FROM messages "
                "WHERE speaker='UNVERIFIED_SUBMISSION' AND status='held' "
                "ORDER BY id LIMIT 100"
            ).fetchall()

    def list_threads(self):
        with closing(self._connect()) as db:
            return db.execute(
                "SELECT t.id,t.created_at,COUNT(m.id),"
                "SUM(CASE WHEN m.status='held' THEN 1 ELSE 0 END),"
                "MAX(m.created_at) FROM threads t LEFT JOIN messages m ON m.thread_id=t.id "
                "GROUP BY t.id ORDER BY MAX(m.id) DESC LIMIT 100"
            ).fetchall()

    def read_thread(self, thread_id: int):
        with closing(self._connect()) as db:
            if not db.execute("SELECT 1 FROM threads WHERE id=?", (thread_id,)).fetchone():
                raise ValueError("Unknown conversation thread")
            rows = db.execute(
                "SELECT id,created_at,speaker,claim,body,status FROM messages "
                "WHERE thread_id=? ORDER BY id DESC LIMIT ?",
                (thread_id, MAX_THREAD_VIEW),
            ).fetchall()
            return list(reversed(rows))

    def review(self, message_id: int, decision: str) -> bool:
        if decision not in {"reviewed", "rejected"}:
            raise ValueError("Decision must be reviewed or rejected")
        with closing(self._connect()) as db:
            with db:
                cursor = db.execute(
                    "UPDATE messages SET status=? WHERE id=? "
                    "AND speaker='UNVERIFIED_SUBMISSION' AND status='held'",
                    (decision, message_id),
                )
                return cursor.rowcount == 1

    def owner_reply(self, thread_id: int, body: str) -> int:
        body = validate_message("Project owner", body)[1]
        with closing(self._connect()) as db:
            with db:
                if not db.execute("SELECT 1 FROM threads WHERE id=?", (thread_id,)).fetchone():
                    raise ValueError("Unknown conversation thread")
                cursor = db.execute(
                    "INSERT INTO messages(created_at,speaker,claim,body,status,thread_id) "
                    "VALUES(?,?,?,?,?,?)",
                    (now(), "PROJECT_OWNER", "", body, "owner", thread_id),
                )
                return int(cursor.lastrowid)


def _page(title: str, content: str) -> bytes:
    return ("""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>God Brain · """ + escape(title) + """</title>
<style>body{background:#111827;color:#eee;font:16px system-ui;max-width:760px;
margin:2rem auto;padding:0 1rem}article,form,.notice{background:#1f2937;
padding:1rem;border-radius:12px;margin:1rem 0;overflow-wrap:anywhere}
.notice{border-left:4px solid #fbbf24}small{color:#bec8d7}
input,textarea{display:block;width:100%;box-sizing:border-box;margin:.5rem 0;
padding:.6rem}button{padding:.7rem 1.2rem}a{color:#93c5fd}
.body{white-space:pre-wrap}</style></head><body><h1>God Brain · Dialogue Room</h1>
""" + content + "</body></html>").encode("utf-8")


def render_home(token: str) -> bytes:
    content = (
        "<article><h2>Open invitation</h2><p>" + escape(INVITATION) + "</p></article>"
        "<p class='notice'>This is a local research prototype. No connection to a "
        "creator or administrator has been verified. Any claimed identity remains "
        "unverified; messages are not interpreted as evidence of their origin.</p>"
        "<h2>Begin a private conversation</h2>"
        "<p>Your text is stored locally and held for operator review, not displayed "
        "on the public page. You receive a private return link; save it, because "
        "losing it means losing access. Anyone with the link can read and reply. "
        "There is no automatic deletion schedule in this prototype.</p>"
        "<form method='post' action='/submit'>"
        "<label>Claimed name<input name='name' maxlength='80' required></label>"
        "<label>Message<textarea name='message' maxlength='2000' rows='5' required></textarea></label>"
        f"<input type='hidden' name='csrf' value='{escape(token)}'>"
        "<button type='submit'>Send privately for review</button></form>"
    )
    return _page("Invitation", content)


def render_thread(messages, token: str, csrf_token: str) -> bytes:
    items = []
    for msg_id, created, speaker, claim, body, status in messages:
        if speaker == "PROJECT_OWNER":
            who = "Project owner (local operator)"
        else:
            who = "Unverified submission — claimed name: " + escape(claim)
        state = ("Held for review" if status == "held" else
                 "Not accepted" if status == "rejected" else
                 "Reviewed" if status == "reviewed" else "Owner response")
        items.append(
            f"<article><small>#{msg_id} · {escape(created)} · {state}</small>"
            f"<h3>{who}</h3><p class='body'>{escape(body)}</p></article>"
        )
    content = (
        "<p class='notice'>Bookmark or save this page's full URL now. It is your "
        "private return link; possession grants access, not identity. "
        "Keep it confidential. This thread does not verify any respondent's origin.</p>"
        "<h2>Your conversation</h2>" + "\n".join(items) +
        "<h2>Follow up</h2><form method='post' action='/reply'>"
        "<label>Claimed name<input name='name' maxlength='80' required></label>"
        "<label>Message<textarea name='message' maxlength='2000' rows='5' required></textarea></label>"
        f"<input type='hidden' name='return_token' value='{escape(token)}'>"
        f"<input type='hidden' name='csrf' value='{escape(csrf_token)}'>"
        "<button type='submit'>Submit follow-up for review</button></form>"
        "<p><small>Showing at most the 200 most recent messages. "
        "Owner replies require local database access; no public owner login exists.</small></p>"
    )
    return _page("Private conversation", content)


def make_server(store: MessageStore, port: int = 8765) -> ThreadingHTTPServer:
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
            self.send_header("Referrer-Policy", "no-referrer")
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
            expected = f"127.0.0.1:{self.server.server_port}"
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
                self.respond(200, render_home(csrf_token), "text/html; charset=utf-8")
            elif self.path.startswith("/t/"):
                token = self.path[3:]
                messages = store.thread_messages(token)
                if messages is None:
                    self.respond(404, b"Unknown return link")
                else:
                    self.respond(
                        200, render_thread(messages, token, csrf_token),
                        "text/html; charset=utf-8",
                    )
            else:
                self.respond(404, b"Not found")

        def do_POST(self):
            if not self.valid_host():
                return
            if self.path not in {"/submit", "/reply"}:
                return self.respond(404, b"Not found")
            expected_origin = f"http://127.0.0.1:{self.server.server_port}"
            origin = self.headers.get("Origin")
            if origin is not None and origin != expected_origin:
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
                return_token = field("return_token") if self.path == "/reply" else None
                receipt = store.submit(field("name"), field("message"), return_token)
            except (ValueError, UnicodeError) as error:
                return self.respond(400, str(error).encode("utf-8"))
            self.respond(303, location=f"/t/{receipt.token}")

    class LocalServer(ThreadingHTTPServer):
        daemon_threads = True

    return LocalServer(("127.0.0.1", port), Handler)


def main():
    parser = argparse.ArgumentParser(description="God Brain local-only dialogue prototype")
    parser.add_argument("--db", type=Path, default=Path("dialogue_room.sqlite3"))
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument(
        "--mode", choices=["serve", "pending", "threads", "read", "review", "reply"],
        default="serve",
    )
    parser.add_argument("--id", type=int, help="Message ID for --mode review")
    parser.add_argument("--decision", choices=["reviewed", "rejected"])
    parser.add_argument("--thread", type=int, help="Thread ID for --mode reply")
    args = parser.parse_args()
    store = MessageStore(args.db)
    if args.mode == "pending":
        for message_id, thread_id, created, name, body in store.pending():
            print(f"message #{message_id} / thread #{thread_id} / {created} / {name}\n{body}\n")
    elif args.mode == "threads":
        for thread_id, created, count, held, latest in store.list_threads():
            print(f"thread #{thread_id} / created {created} / messages {count} "
                  f"/ held {held} / last activity {latest}")
    elif args.mode == "read":
        if args.thread is None:
            parser.error("--mode read requires --thread")
        try:
            rows = store.read_thread(args.thread)
        except ValueError as error:
            parser.error(str(error))
        for message_id, created, speaker, claim, body, status in rows:
            print(f"#{message_id} / {created} / {speaker} / {claim} / {status}\n{body}\n")
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
        server = make_server(store, args.port)
        print(f"Local-only dialogue room: http://127.0.0.1:{server.server_port}")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            server.server_close()


if __name__ == "__main__":
    main()

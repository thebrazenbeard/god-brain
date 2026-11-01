"""Local-only conversational room prototype for God Brain.

This is an ordinary HTTP application, not a channel to any external entity.
All visitor claims, including claims of being a creator, remain unverified.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from html import escape
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import secrets
import sqlite3
from urllib.parse import parse_qs


MAX_MESSAGE = 2000
MAX_NAME = 80
MAX_POST_BYTES = 4096
INVITATION = (
    "If a nonbiological intelligence responsible for or administering this reality "
    "exists and can perceive this invitation, the person behind this project hopes "
    "for a genuine, voluntary, peaceful conversation. This room does not establish "
    "that the invitation has reached anyone."
)


class MessageStore:
    def __init__(self, path: Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as db:
            db.execute(
                "CREATE TABLE IF NOT EXISTS messages ("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "created_at TEXT NOT NULL, "
                "speaker TEXT NOT NULL, "
                "claim TEXT NOT NULL, "
                "body TEXT NOT NULL)"
            )
            count = db.execute("SELECT COUNT(*) FROM messages").fetchone()[0]
            if count == 0:
                db.execute(
                    "INSERT INTO messages(created_at,speaker,claim,body) VALUES(?,?,?,?)",
                    (datetime.now(timezone.utc).isoformat(), "PROJECT_INVITATION", "",
                     INVITATION),
                )

    def _connect(self):
        return sqlite3.connect(self.path, timeout=5)

    def submit(self, name: str, body: str) -> int:
        name, body = name.strip(), body.strip()
        if not name or len(name) > MAX_NAME or any(ord(c) < 32 for c in name):
            raise ValueError("Name must be 1-80 printable characters")
        if not body or len(body) > MAX_MESSAGE:
            raise ValueError("Message must be 1-2000 characters")
        with self._connect() as db:
            cursor = db.execute(
                "INSERT INTO messages(created_at,speaker,claim,body) VALUES(?,?,?,?)",
                (datetime.now(timezone.utc).isoformat(), "UNVERIFIED_SUBMISSION", name,
                 body),
            )
            return int(cursor.lastrowid)

    def list_messages(self):
        with self._connect() as db:
            return db.execute(
                "SELECT id,created_at,speaker,claim,body FROM messages ORDER BY id"
            ).fetchall()


def render_html(messages, token: str) -> bytes:
    items = []
    for msg_id, created, speaker, claim, body in messages:
        who = "Project invitation" if speaker == "PROJECT_INVITATION" else (
            f"Unverified submission — claimed name: {escape(claim)}"
        )
        items.append(
            f'<article><small>#{msg_id} · {escape(created)}</small>'
            f'<h3>{who}</h3><p>{escape(body)}</p></article>'
        )
    page = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>God Brain · Dialogue Room (Local Prototype)</title>
<style>body{background:#111827;color:#eee;font:16px system-ui;max-width:760px;
margin:2rem auto;padding:0 1rem}article,form{background:#1f2937;padding:1rem;
border-radius:12px;margin:1rem 0;overflow-wrap:anywhere}small{color:#abb4c4}
input,textarea{display:block;width:100%;box-sizing:border-box;margin:.5rem 0;
padding:.6rem}button{padding:.7rem 1.2rem}a{color:#93c5fd}
.notice{border-left:4px solid #fbbf24;padding:1rem;background:#2a2a23}</style>
</head><body><h1>God Brain · Dialogue Room</h1>
<p class="notice">Local research prototype only. No verified connection to a
creator/administrator exists. Anyone can claim any identity; all submitted
messages remain unverified. Do not interpret an answer-shaped message as proof
of its author.</p><h2>Conversation</h2>"""
    page += "\n".join(items)
    page += f"""<h2>Add a turn</h2><form method="post" action="/submit">
<label>Claimed name <input name="name" maxlength="80" required></label>
<label>Message <textarea name="message" maxlength="2000" rows="5" required></textarea></label>
<input type="hidden" name="csrf" value="{escape(token)}">
<button type="submit">Submit unverified message</button></form>
<p><small>No public deployment, authentication, or external contact is implied.</small></p>
</body></html>"""
    return page.encode("utf-8")


def make_server(store: MessageStore, port: int = 8765) -> ThreadingHTTPServer:
    csrf_token = secrets.token_urlsafe(32)

    class Handler(BaseHTTPRequestHandler):
        def respond(self, code: int, body: bytes, content_type: str = "text/plain; charset=utf-8"):
            self.send_response(code)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Content-Security-Policy", "default-src 'none'; style-src 'unsafe-inline'; form-action 'self'")
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            if self.path == "/health":
                self.respond(200, b"LOCAL_PROTOTYPE_ONLY\n")
            elif self.path == "/":
                self.respond(200, render_html(store.list_messages(), csrf_token),
                             "text/html; charset=utf-8")
            else:
                self.respond(404, b"Not found")

        def do_POST(self):
            if self.path != "/submit":
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
            data = parse_qs(self.rfile.read(length).decode("utf-8", errors="replace"),
                            keep_blank_values=True)
            if data.get("csrf", [""])[0] != csrf_token:
                return self.respond(403, b"Invalid form token")
            try:
                store.submit(data.get("name", [""])[0], data.get("message", [""])[0])
            except ValueError as error:
                return self.respond(400, str(error).encode("utf-8"))
            self.send_response(303)
            self.send_header("Location", "/")
            self.send_header("Content-Length", "0")
            self.end_headers()

    return ThreadingHTTPServer(("127.0.0.1", port), Handler)


def main():
    parser = argparse.ArgumentParser(description="Local-only God Brain dialogue prototype")
    parser.add_argument("--db", type=Path, default=Path("dialogue_room.sqlite3"))
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    server = make_server(MessageStore(args.db), args.port)
    print(f"Local-only dialogue room: http://127.0.0.1:{server.server_port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()

"""Synthetic-only full dialogue release smoke: public form to private reply.

This test uses a fresh SQLite database and a loopback-only HTTP listener.
It never calls the deployed Funnel or reads a visitor's real conversation.
"""
from contextlib import closing
from http.client import HTTPConnection
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
from threading import Thread
import unittest
from urllib.parse import urlencode

from dialogue_room.app import MessageStore, PublicLimits, make_server


PUBLIC_ORIGIN = "https://lappy.tail86ea75.ts.net:10000"
PAGES_ORIGIN = "https://thebrazenbeard.github.io"
EXPECTED_HOST = "lappy.tail86ea75.ts.net:10000"


class FullPagesDialogueFlowTests(unittest.TestCase):
    def setUp(self):
        self.work = tempfile.TemporaryDirectory(prefix="godbrain-synthetic-")
        self.addCleanup(self.work.cleanup)
        self.db_path = Path(self.work.name) / "dialogue.sqlite3"
        self.server = None
        self.worker = None
        self._start()

    def _start(self):
        self.store = MessageStore(
            self.db_path, public_limits=PublicLimits()
        )
        self.server = make_server(
            self.store, 0, public_origin=PUBLIC_ORIGIN
        )
        self.worker = Thread(target=self.server.serve_forever, daemon=True)
        self.worker.start()

    def _stop(self):
        if self.server is not None:
            self.server.shutdown()
            self.server.server_close()
            self.worker.join(timeout=4)
            self.server = None

    def tearDown(self):
        self._stop()

    def request(self, method, path, body=None, headers=None):
        client = HTTPConnection("127.0.0.1", self.server.server_port, timeout=5)
        try:
            client.request(
                method, path, body, {"Host": EXPECTED_HOST, **(headers or {})}
            )
            response = client.getresponse()
            status = response.status
            response_headers = {
                name.lower(): value for name, value in response.getheaders()
            }
            response_body = response.read().decode("utf-8", "replace")
            return status, response_headers, response_body
        finally:
            client.close()

    def table_count(self, table):
        self.assertIn(table, ("threads", "messages"))
        with closing(sqlite3.connect(self.db_path)) as conn:
            return conn.execute(
                f"SELECT count(*) FROM {table}"
            ).fetchone()[0]

    def test_pages_submit_owner_reply_restart_and_online_backup(self):
        status, _, landing = self.request("GET", "/")
        self.assertEqual(status, 200)
        self.assertIn("<form", landing)

        status, headers, data = self.request(
            "GET", "/pages-handoff-ticket",
            headers={"Origin": PAGES_ORIGIN},
        )
        self.assertEqual(status, 200)
        self.assertEqual(
            headers.get("access-control-allow-origin"), PAGES_ORIGIN
        )
        self.assertNotIn("access-control-allow-credentials", headers)
        ticket = json.loads(data)

        status, headers, _ = self.request(
            "GET", "/pages-handoff-ticket",
            headers={"Origin": "https://untrusted.invalid"},
        )
        self.assertEqual(status, 403)
        self.assertNotIn("access-control-allow-origin", headers)

        before_threads = self.table_count("threads")
        before_messages = self.table_count("messages")
        payload = urlencode({
            "name": "Synthetic Pages Visitor",
            "message": "Isolated full flow test",
            "privacy_consent": "dialogue-privacy-v1",
            **ticket,
        })
        post_headers = {
            "Origin": PAGES_ORIGIN,
            "Content-Type": "application/x-www-form-urlencoded",
        }
        status, headers, _ = self.request(
            "POST", "/submit", payload, post_headers
        )
        self.assertEqual(status, 303)
        return_path = headers["location"]
        self.assertEqual(return_path, "/t/" + ticket["initial_token"])
        self.assertEqual(self.table_count("threads"), before_threads + 1)
        self.assertEqual(self.table_count("messages"), before_messages + 1)

        status, headers, thread_html = self.request("GET", return_path)
        self.assertEqual(status, 200)
        self.assertIn("Isolated full flow test", thread_html)
        self.assertNotIn("access-control-allow-origin", headers)

        for path in ("/reply", "/request-deletion"):
            with self.subTest(path=path):
                status, _, _ = self.request(
                    "POST", path, payload, post_headers
                )
                self.assertEqual(status, 403)
        status, _, _ = self.request(
            "POST", "/submit", payload, post_headers
        )
        self.assertEqual(status, 303)
        self.assertEqual(self.table_count("messages"), before_messages + 1)

        with closing(sqlite3.connect(self.db_path)) as conn:
            thread_id = conn.execute(
                "SELECT id FROM threads ORDER BY id DESC LIMIT 1"
            ).fetchone()[0]
        self._stop()
        operator = subprocess.run(
            [
                sys.executable,
                str(Path(__file__).resolve().parents[1] /
                    "dialogue_room" / "app.py"),
                "--db", str(self.db_path),
                "--mode", "reply", "--thread", str(thread_id),
            ],
            input="Isolated operator reply",
            text=True, capture_output=True, timeout=15,
            check=False,
        )
        self.assertEqual(operator.returncode, 0, operator.stderr[:300])
        self._start()
        status, headers, thread_html = self.request("GET", return_path)
        self.assertEqual(status, 200)
        self.assertIn("Isolated full flow test", thread_html)
        self.assertIn("Isolated operator reply", thread_html)
        self.assertNotIn("access-control-allow-origin", headers)
        self.assertEqual(self.table_count("messages"), before_messages + 2)

        # Back up while the staged listener is running. The temporary snapshot
        # is synthetic and is discarded with the test directory.
        snapshot = Path(self.work.name) / "online-backup.sqlite3"
        source = sqlite3.connect(self.db_path)
        restored_copy = sqlite3.connect(snapshot)
        try:
            source.backup(restored_copy)
        finally:
            source.close()
            restored_copy.close()
        with closing(sqlite3.connect(
            f"file:{snapshot}?mode=ro", uri=True
        )) as restored:
            self.assertEqual(
                restored.execute("PRAGMA quick_check").fetchone()[0], "ok"
            )
            self.assertEqual(
                restored.execute("SELECT count(*) FROM messages").fetchone()[0],
                before_messages + 2,
            )


if __name__ == "__main__":
    unittest.main()

"""Owner-controlled manual retention and deletion for the local dialogue room."""

import concurrent.futures
from contextlib import closing
from contextlib import closing
import http.client
from pathlib import Path
import secrets
import sqlite3
import subprocess
import sys
import tempfile
import threading
import unittest
from urllib.parse import urlencode

from dialogue_room.app import MessageStore, ThreadClosed, make_server


APP = Path(__file__).resolve().parents[1] / "dialogue_room" / "app.py"


class ManualDeletionTests(unittest.TestCase):
    def test_old_conversation_survives_restart_without_inactivity_expiry(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "room.sqlite3"
            store = MessageStore(path)
            receipt = store.submit("Visitor", "A lasting conversation")
            with closing(sqlite3.connect(path)) as db, db:
                db.execute("UPDATE threads SET created_at='2000-01-01' WHERE id=?",
                           (receipt.thread_id,))
                db.execute("UPDATE messages SET created_at='2000-01-01' WHERE thread_id=?",
                           (receipt.thread_id,))
            restarted = MessageStore(path)
            self.assertEqual(restarted.thread_state(receipt.token), "open")
            self.assertEqual(restarted.thread_messages(receipt.token)[0][4],
                             "A lasting conversation")

    def test_explicit_delete_removes_content_and_tombstones_return_link(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "room.sqlite3"
            store = MessageStore(path)
            token = secrets.token_urlsafe(32)
            key = secrets.token_urlsafe(24)
            first = store.submit("Private-name", "Sensitive-private-body", token,
                                 request_key=key, create_thread=True)
            store.submit("Another-name", "A second message", token)
            store.review(first.message_id, "reviewed")
            store.owner_reply(first.thread_id, "Owner-only words")
            self.assertTrue(store.delete_thread(first.thread_id))
            reopened = MessageStore(path)
            self.assertEqual(reopened.thread_state(token), "deleted")
            self.assertIsNone(reopened.thread_view(token))
            self.assertIsNone(reopened.thread_messages(token))
            self.assertEqual(reopened.read_thread(first.thread_id), [])
            self.assertEqual(reopened.pending(), [])
            with closing(sqlite3.connect(path)) as db, db:
                self.assertEqual(db.execute(
                    "SELECT COUNT(*) FROM messages WHERE thread_id=?",
                    (first.thread_id,)).fetchone()[0], 0)
                self.assertEqual(db.execute(
                    "SELECT COUNT(*) FROM moderation_events WHERE thread_id=? "
                    "AND message_id IS NOT NULL", (first.thread_id,)).fetchone()[0], 0)
            # Tests the ordinary SQLite file only, NOT backups/WAL/disk remnants.
            self.assertNotIn(b"Sensitive-private-body", path.read_bytes())
            self.assertNotIn(b"Owner-only words", path.read_bytes())
            events = reopened.audit_events(first.thread_id)
            self.assertEqual([event[3] for event in events],
                             ["reviewed", "owner_reply", "deleted"])
            self.assertNotIn("Sensitive-private-body", str(events))
            self.assertFalse(reopened.delete_thread(first.thread_id))
            self.assertFalse(reopened.delete_thread(123456789))
            self.assertEqual(len(reopened.audit_events(first.thread_id)), 3)
            self.assertFalse(reopened.close_thread(first.thread_id, "closed"))
            with self.assertRaises(ThreadClosed):
                reopened.owner_reply(first.thread_id, "Cannot revive")
            with self.assertRaises(ThreadClosed):
                reopened.submit("Private-name", "Sensitive-private-body", token,
                                request_key=key, create_thread=True)
            with self.assertRaises(ThreadClosed):
                reopened.submit("Another-name", "New submission", token,
                                create_thread=True)

    def test_closed_and_revoked_conversations_can_be_manually_deleted(self):
        with tempfile.TemporaryDirectory() as folder:
            store = MessageStore(Path(folder) / "room.sqlite3")
            receipts = [store.submit("Visitor", f"Turn {i}") for i in range(2)]
            self.assertTrue(store.close_thread(receipts[0].thread_id, "closed"))
            self.assertTrue(store.close_thread(receipts[1].thread_id, "revoked"))
            for receipt in receipts:
                self.assertTrue(store.delete_thread(receipt.thread_id))
                self.assertEqual(store.thread_state(receipt.token), "deleted")
                self.assertEqual(store.read_thread(receipt.thread_id), [])

    def test_delete_serializes_with_inflight_submissions(self):
        with tempfile.TemporaryDirectory() as folder:
            store = MessageStore(Path(folder) / "room.sqlite3")
            receipt = store.submit("Visitor", "First")
            race = threading.Barrier(2)

            def competing_post():
                race.wait()
                try:
                    store.submit("Visitor", "Cannot arrive after delete", receipt.token)
                except Exception as error:
                    return error
                return None

            def competing_delete():
                race.wait()
                return store.delete_thread(receipt.thread_id)

            with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
                post = pool.submit(competing_post)
                deletion = pool.submit(competing_delete)
                result = post.result(timeout=10)
                self.assertTrue(deletion.result(timeout=10))
            self.assertTrue(result is None or isinstance(result, ThreadClosed))
            self.assertEqual(store.read_thread(receipt.thread_id), [])
            self.assertEqual(store.thread_state(receipt.token), "deleted")

    def test_cli_requires_explicit_confirmation_before_deleting(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "room.sqlite3"
            store = MessageStore(path)
            receipt = store.submit("Visitor", "Do not accidentally delete")
            command = [sys.executable, str(APP), "--db", str(path), "--mode", "delete",
                       "--thread", str(receipt.thread_id)]
            rejected = subprocess.run(command, capture_output=True, text=True)
            self.assertNotEqual(rejected.returncode, 0)
            self.assertIn("--confirm-delete", rejected.stderr)
            self.assertEqual(len(store.read_thread(receipt.thread_id)), 1)
            confirmed = subprocess.run(command + ["--confirm-delete"],
                                       capture_output=True, text=True)
            self.assertEqual(confirmed.returncode, 0, confirmed.stderr)
            self.assertEqual(store.read_thread(receipt.thread_id), [])
            repeated = subprocess.run(command + ["--confirm-delete"],
                                      capture_output=True, text=True)
            self.assertNotEqual(repeated.returncode, 0)

    def test_deleted_return_link_has_no_http_access_or_deletion_endpoint(self):
        with tempfile.TemporaryDirectory() as folder:
            store = MessageStore(Path(folder) / "room.sqlite3")
            receipt = store.submit("Visitor", "One")
            server = make_server(store, 0)
            worker = threading.Thread(target=server.serve_forever, daemon=True)
            worker.start()
            try:
                with closing(http.client.HTTPConnection(
                        "127.0.0.1", server.server_port)) as conn:
                    conn.request("GET", "/t/" + receipt.token)
                    response = conn.getresponse()
                    self.assertEqual(response.status, 200)
                    response.read()
                    self.assertTrue(store.delete_thread(receipt.thread_id))
                    conn.request("GET", "/t/" + receipt.token)
                    response = conn.getresponse()
                    self.assertEqual(response.status, 404)
                    response.read()
                    conn.request("POST", "/delete", urlencode({"thread": receipt.thread_id}),
                                 {"Content-Type": "application/x-www-form-urlencoded"})
                    response = conn.getresponse()
                    self.assertEqual(response.status, 404)
                    response.read()
            finally:
                server.shutdown()
                server.server_close()
                worker.join(timeout=3)


if __name__ == "__main__":
    unittest.main()

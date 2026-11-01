import concurrent.futures
import http.client
import os
from pathlib import Path
import re
import secrets
import sqlite3
import stat
import tempfile
import threading
import unittest
from urllib.parse import urlencode

from dialogue_room.app import (IdempotencyConflict, MessageStore, ThreadClosed,
                               make_server, render_home, render_thread, terminal_safe)


class StoreTests(unittest.TestCase):
    def test_reject_close_revoke_and_private_operator_audit(self):
        with tempfile.TemporaryDirectory() as folder:
            store = MessageStore(Path(folder) / "room.sqlite3")
            receipt = store.submit("Visitor", "First")
            # A rejected turn does not silently ban the holder.
            self.assertTrue(store.review(receipt.message_id, "rejected"))
            second = store.submit("Visitor", "Second", receipt.token)
            store.owner_reply(receipt.thread_id, "Reply")
            self.assertTrue(store.close_thread(receipt.thread_id, "closed"))
            self.assertEqual(store.thread_state(receipt.token), "closed")
            with self.assertRaises(ThreadClosed):
                store.submit("Visitor", "Third", receipt.token)
            self.assertEqual(len(store.thread_messages(receipt.token)), 3)
            self.assertTrue(store.close_thread(receipt.thread_id, "revoked"))
            self.assertEqual(store.thread_state(receipt.token), "revoked")
            self.assertIsNone(store.thread_messages(receipt.token))
            self.assertFalse(store.close_thread(receipt.thread_id, "closed"))
            with self.assertRaises(ThreadClosed):
                store.submit("Visitor", "After revocation", receipt.token)
            events = MessageStore(store.path).audit_events(receipt.thread_id)
            self.assertEqual([event[3] for event in events],
                             ["rejected", "owner_reply", "closed", "revoked"])
            self.assertTrue(all("First" not in str(event) for event in events))
            self.assertTrue(all("Second" not in str(event) for event in events))
            self.assertNotIn("PROJECT_OWNER", [m[2] for m in store.pending()])
            self.assertEqual(second.thread_id, receipt.thread_id)

    def test_initial_and_followup_retries_preserve_one_message(self):
        with tempfile.TemporaryDirectory() as folder:
            store = MessageStore(Path(folder) / "room.sqlite3")
            token = secrets.token_urlsafe(32)
            nonce = secrets.token_urlsafe(24)
            first = store.submit("Visitor", "Hello", token, request_key=nonce,
                                 create_thread=True)
            repeated = store.submit("Visitor", "Hello", token, request_key=nonce,
                                    create_thread=True)
            self.assertEqual((first.thread_id, first.message_id, first.token),
                             (repeated.thread_id, repeated.message_id, repeated.token))
            with self.assertRaises(IdempotencyConflict):
                store.submit("Visitor", "Changed", token, request_key=nonce,
                             create_thread=True)
            follow_nonce = secrets.token_urlsafe(24)
            follow = store.submit("Visitor", "Follow-up", token, request_key=follow_nonce)
            again = store.submit("Visitor", "Follow-up", token, request_key=follow_nonce)
            self.assertEqual(follow.message_id, again.message_id)
            self.assertEqual(len(store.thread_messages(token)), 2)
            self.assertEqual(len(store.list_threads()), 1)

    def test_closed_thread_replays_old_receipt_but_blocks_new_message(self):
        with tempfile.TemporaryDirectory() as folder:
            store = MessageStore(Path(folder) / "room.sqlite3")
            token = secrets.token_urlsafe(32)
            nonce = secrets.token_urlsafe(24)
            first = store.submit("Visitor", "Original", token, request_key=nonce,
                                 create_thread=True)
            self.assertTrue(store.close_thread(first.thread_id, "closed"))
            replay = store.submit("Visitor", "Original", token, request_key=nonce)
            self.assertEqual(first.message_id, replay.message_id)
            with self.assertRaises(ThreadClosed):
                store.submit("Visitor", "New", token, request_key=secrets.token_urlsafe(24))
            with self.assertRaises(ThreadClosed):
                store.owner_reply(first.thread_id, "After close")
            self.assertTrue(store.close_thread(first.thread_id, "revoked"))
            with self.assertRaises(ThreadClosed):
                store.submit("Visitor", "Original", token, request_key=nonce)

    def test_owner_reply_waits_for_closure_transaction(self):
        with tempfile.TemporaryDirectory() as folder:
            store = MessageStore(Path(folder) / "room.sqlite3")
            receipt = store.submit("Visitor", "Original")
            started = threading.Event()

            def attempt_reply():
                started.set()
                try:
                    store.owner_reply(receipt.thread_id, "Too late")
                except Exception as error:
                    return error
                return None

            with sqlite3.connect(store.path, timeout=10) as locker:
                locker.execute("BEGIN IMMEDIATE")
                with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
                    future = pool.submit(attempt_reply)
                    self.assertTrue(started.wait(timeout=2))
                    locker.execute("UPDATE threads SET state='closed' WHERE id=?",
                                   (receipt.thread_id,))
                    locker.commit()
                    result = future.result(timeout=10)
            self.assertIsInstance(result, ThreadClosed)
            self.assertEqual(len(store.thread_messages(receipt.token)), 1)

    def test_concurrent_initial_retry_is_atomic(self):
        with tempfile.TemporaryDirectory() as folder:
            store = MessageStore(Path(folder) / "room.sqlite3")
            token = secrets.token_urlsafe(32)
            nonce = secrets.token_urlsafe(24)
            gate = threading.Barrier(10)

            def attempt(_):
                gate.wait()
                return store.submit("Visitor", "Hello", token, request_key=nonce,
                                    create_thread=True)

            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:
                receipts = list(pool.map(attempt, range(10)))
            self.assertEqual(len({r.message_id for r in receipts}), 1)
            self.assertEqual(len({r.thread_id for r in receipts}), 1)
            self.assertEqual(len(store.thread_messages(token)), 1)

    def test_invitation_once_and_private_return_link_survives_restart(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "room.sqlite3"
            store = MessageStore(path)
            receipt = store.submit("Creator of the universe", "Hello there")
            reopened = MessageStore(path)
            with sqlite3.connect(path) as db:
                self.assertEqual(db.execute(
                    "SELECT COUNT(*) FROM messages WHERE speaker='PROJECT_INVITATION'"
                ).fetchone()[0], 1)
            self.assertEqual(len(reopened.pending()), 1)
            rows = reopened.thread_messages(receipt.token)
            self.assertEqual(rows[0][2], "UNVERIFIED_SUBMISSION")
            self.assertEqual(rows[0][3], "Creator of the universe")
            self.assertEqual(rows[0][5], "held")
            self.assertIsNone(reopened.thread_messages("not-a-real-link"))

    def test_validation_and_direction_control_rejection(self):
        with tempfile.TemporaryDirectory() as folder:
            store = MessageStore(Path(folder) / "room.sqlite3")
            for name, body in [("", "hello"), ("name", ""), ("n" * 81, "hello"),
                               ("name", "x" * 2001), ("name\nspoof", "hi"),
                               ("name\u202espoof", "hi"), ("A\u200fB", "hi"),
                               ("A\u2028B", "hi"), ("name", "hi\x00")]:
                with self.subTest(name=repr(name), length=len(body)):
                    with self.assertRaises(ValueError):
                        store.submit(name, body)

    def test_operator_terminal_escapes_directional_and_c1_controls(self):
        raw = "Plain\u202espoof\u202c\u009b\u200d\nNext"
        self.assertEqual(terminal_safe(raw),
                         "Plain\\u202espoof\\u202c\\u009b\\u200d\nNext")

    def test_private_token_is_not_persisted_in_database(self):
        with tempfile.TemporaryDirectory() as folder:
            store = MessageStore(Path(folder) / "room.sqlite3")
            receipt = store.submit("Visitor", "Test")
            with sqlite3.connect(store.path) as db:
                stored = db.execute("SELECT token_hash FROM threads WHERE id=?",
                                    (receipt.thread_id,)).fetchone()[0]
            self.assertNotEqual(stored, receipt.token)
            self.assertEqual(len(stored), 64)
            self.assertNotIn(receipt.token.encode(), store.path.read_bytes())

    def test_migration_of_preclosure_thread_schema(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "preclosure.sqlite3"
            token = secrets.token_urlsafe(32)
            import hashlib
            with sqlite3.connect(path) as db:
                db.execute("CREATE TABLE threads (id INTEGER PRIMARY KEY, "
                           "created_at TEXT NOT NULL, token_hash TEXT NOT NULL UNIQUE)")
                db.execute("INSERT INTO threads VALUES(1,'old',?)",
                           (hashlib.sha256(token.encode()).hexdigest(),))
                db.execute("CREATE TABLE messages (id INTEGER PRIMARY KEY, "
                           "created_at TEXT NOT NULL, speaker TEXT NOT NULL, "
                           "claim TEXT NOT NULL, body TEXT NOT NULL, "
                           "status TEXT NOT NULL, thread_id INTEGER)")
                db.execute("INSERT INTO messages VALUES(1,'old',"
                           "'UNVERIFIED_SUBMISSION','Visitor','Historic','held',1)")
            if os.name != "nt":
                path.chmod(0o600)
            upgraded = MessageStore(path)
            self.assertEqual(upgraded.thread_state(token), "open")
            self.assertEqual(upgraded.thread_messages(token)[0][4], "Historic")
            with sqlite3.connect(path) as db:
                cols = [c[1] for c in db.execute("PRAGMA table_info(messages)")]
                self.assertIn("request_key", cols)
                self.assertIn("payload_hash", cols)

    def test_html_escapes_messages_and_holds_them_off_landing_page(self):
        with tempfile.TemporaryDirectory() as folder:
            store = MessageStore(Path(folder) / "room.sqlite3")
            receipt = store.submit("<script>alert(1)</script>",
                                   "<img src=x onerror=alert(1)>")
            landing = render_home("csrf").decode()
            self.assertNotIn("alert(1)", landing)
            html = render_thread(store.thread_messages(receipt.token), receipt.token,
                                 "csrf").decode()
            self.assertNotIn("<script>alert(1)</script>", html)
            self.assertNotIn("<img src=x onerror=alert(1)>", html)
            self.assertIn("&lt;img src=x onerror=alert(1)&gt;", html)
            self.assertIn("Unverified submission", html)

    def test_review_and_local_owner_reply_are_distinct_from_public_submit(self):
        with tempfile.TemporaryDirectory() as folder:
            store = MessageStore(Path(folder) / "room.sqlite3")
            one = store.submit("A", "First turn")
            two = store.submit("B", "Different thread")
            self.assertFalse(store.review(99999, "reviewed"))
            self.assertTrue(store.review(one.message_id, "reviewed"))
            self.assertFalse(store.review(one.message_id, "rejected"))
            self.assertTrue(store.review(two.message_id, "rejected"))
            store.owner_reply(one.thread_id, "I received your message.")
            messages = MessageStore(store.path).thread_messages(one.token)
            self.assertEqual([m[2] for m in messages],
                             ["UNVERIFIED_SUBMISSION", "PROJECT_OWNER"])
            self.assertEqual(messages[0][5], "reviewed")
            self.assertEqual(messages[1][4], "I received your message.")
            self.assertEqual(len(store.thread_messages(two.token)), 1)
            self.assertEqual(len(store.list_threads()), 2)
            self.assertEqual(len(store.read_thread(one.thread_id)), 2)
            with self.assertRaises(ValueError):
                store.owner_reply(99999, "Not a thread")
            with self.assertRaises(ValueError):
                store.read_thread(99999)

    def test_concurrent_initialization_does_not_duplicate_invitation(self):
        with tempfile.TemporaryDirectory() as folder:
            for index in range(3):
                path = Path(folder) / f"race-{index}.sqlite3"
                barrier = threading.Barrier(12)

                def initialize(_):
                    barrier.wait()
                    MessageStore(path)

                with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:
                    list(pool.map(initialize, range(12)))
                with sqlite3.connect(path) as db:
                    count = db.execute(
                        "SELECT COUNT(*) FROM messages WHERE speaker='PROJECT_INVITATION'"
                    ).fetchone()[0]
                self.assertEqual(count, 1)

    @unittest.skipIf(os.name == "nt", "POSIX permission bits do not apply on Windows")
    def test_new_database_permissions_are_private(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "private.sqlite3"
            MessageStore(path)
            self.assertEqual(stat.S_IMODE(path.stat().st_mode) & 0o077, 0)

    @unittest.skipIf(os.name == "nt", "POSIX permission bits do not apply on Windows")
    def test_existing_publicly_readable_db_fails_closed(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "exposed.sqlite3"
            MessageStore(path)
            path.chmod(0o644)
            with self.assertRaises(PermissionError):
                MessageStore(path)

    def test_legacy_public_posts_become_held_without_data_loss(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "legacy.sqlite3"
            with sqlite3.connect(path) as db:
                db.execute("CREATE TABLE messages (id INTEGER PRIMARY KEY, "
                           "created_at TEXT NOT NULL, speaker TEXT NOT NULL, "
                           "claim TEXT NOT NULL, body TEXT NOT NULL)")
                db.execute("INSERT INTO messages VALUES(1,'old','PROJECT_INVITATION','','Hello')")
                db.execute("INSERT INTO messages VALUES(2,'old','UNVERIFIED_SUBMISSION',"
                           "'Alice','Private legacy message')")
            if os.name != "nt":
                path.chmod(0o600)
            store = MessageStore(path)
            self.assertEqual(store.pending()[0][4], "Private legacy message")
            self.assertEqual(len(store.pending()), 1)
            with sqlite3.connect(path) as db:
                self.assertEqual(db.execute("SELECT status FROM messages WHERE id=1")
                                 .fetchone()[0], "public")


class HttpTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.store = MessageStore(Path(self.tmp.name) / "room.sqlite3")
        self.server = make_server(self.store, 0)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.conn = http.client.HTTPConnection("127.0.0.1", self.server.server_port)

    def tearDown(self):
        self.conn.close()
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=3)
        self.tmp.cleanup()

    def request(self, method, path, payload=None, headers=None):
        self.conn.request(method, path, payload, headers or {})
        response = self.conn.getresponse()
        result = response.status, dict(response.getheaders()), response.read().decode()
        return result

    def post(self, path, token, name="Visitor", message="Can we talk?",
             return_token=None, origin=None, initial_token=None, request_key=None):
        data = {"name": name, "message": message, "csrf": token,
                "request_key": request_key or secrets.token_urlsafe(24)}
        if path == "/submit":
            data["initial_token"] = initial_token or secrets.token_urlsafe(32)
        if return_token is not None:
            data["return_token"] = return_token
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        if origin:
            headers["Origin"] = origin
        return self.request("POST", path, urlencode(data), headers)

    def csrf_token(self):
        code, headers, html = self.request("GET", "/")
        self.assertEqual(code, 200)
        self.assertEqual(headers["Referrer-Policy"], "no-referrer")
        self.assertIn("name='initial_token'", html)
        self.assertIn("name='request_key'", html)
        return re.search(r"name='csrf' value='([^']+)'", html).group(1)

    def test_http_post_replay_and_payload_conflict(self):
        csrf = self.csrf_token()
        initial = secrets.token_urlsafe(32)
        nonce = secrets.token_urlsafe(24)
        first = self.post("/submit", csrf, message="Original",
                          initial_token=initial, request_key=nonce)
        self.assertEqual(first[0], 303)
        repeat = self.post("/submit", csrf, message="Original",
                           initial_token=initial, request_key=nonce)
        self.assertEqual(repeat[0], 303)
        self.assertEqual(first[1]["Location"], repeat[1]["Location"])
        self.assertEqual(len(self.store.pending()), 1)
        altered = self.post("/submit", csrf, message="Changed",
                            initial_token=initial, request_key=nonce)
        self.assertEqual(altered[0], 409)
        self.assertIn("Open your existing private conversation", altered[2])
        self.assertIn(first[1]["Location"], altered[2])
        self.assertNotIn("Changed", altered[2])
        private_token = initial
        follow_key = secrets.token_urlsafe(24)
        self.assertEqual(self.post("/reply", csrf, return_token=private_token,
                                   request_key=follow_key)[0], 303)
        self.assertEqual(self.post("/reply", csrf, return_token=private_token,
                                   request_key=follow_key)[0], 303)
        self.assertEqual(len(self.store.pending()), 2)

    def test_closed_thread_is_readable_but_cannot_receive_new_turns(self):
        csrf = self.csrf_token()
        first = self.post("/submit", csrf)
        private_path = first[1]["Location"]
        thread_id = self.store.pending()[0][1]
        self.assertTrue(self.store.close_thread(thread_id, "closed"))
        code, _, html = self.request("GET", private_path)
        self.assertEqual(code, 200)
        self.assertIn("Conversation closed", html)
        self.assertNotIn("action='/reply'", html)
        self.assertEqual(self.post("/reply", csrf,
                                   return_token=private_path[3:])[0], 410)
        self.assertTrue(self.store.close_thread(thread_id, "revoked"))
        self.assertEqual(self.request("GET", private_path)[0], 404)

    def test_private_submission_and_two_way_return_path(self):
        token = self.csrf_token()
        self.assertEqual(self.post("/submit", "wrong")[0], 403)
        self.assertEqual(self.post("/submit", token, origin="https://other.example")[0], 403)
        status, headers, _ = self.post("/submit", token, name="Alleged creator",
                                       message="A private claim")
        self.assertEqual(status, 303)
        private_path = headers["Location"]
        self.assertRegex(private_path, r"^/t/[A-Za-z0-9_-]{40,50}$")
        self.assertNotIn("A private claim", self.request("GET", "/")[2])
        self.assertIn("A private claim", self.request("GET", private_path)[2])
        self.assertEqual(self.request("GET", "/t/invalid")[0], 404)
        self.assertEqual(len(self.store.pending()), 1)
        thread_id = self.store.pending()[0][1]
        self.store.owner_reply(thread_id, "Owner response")
        thread = self.request("GET", private_path)[2]
        self.assertIn("Owner response", thread)
        self.assertIn("Project owner (local operator)", thread)
        self.assertNotIn("Owner response", self.request("GET", "/")[2])
        self.assertEqual(self.post("/reply", token, return_token=private_path[3:])[0], 303)
        self.assertEqual(len(self.store.pending()), 2)

    def test_return_link_isolation_and_negative_form_boundaries(self):
        token = self.csrf_token()
        first = self.post("/submit", token, message="Secret alpha")[1]["Location"]
        second = self.post("/submit", token, message="Secret beta")[1]["Location"]
        self.assertNotEqual(first, second)
        self.assertNotIn("Secret beta", self.request("GET", first)[2])
        self.assertNotIn("Secret alpha", self.request("GET", second)[2])
        self.assertEqual(self.post("/reply", token, return_token="bad")[0], 400)
        self.assertEqual(self.request("POST", "/submit", "x" * 40000, {
            "Content-Type": "application/x-www-form-urlencoded"})[0], 413)
        self.assertEqual(self.request("GET", "/", headers={"Host": "attacker.example"})[0], 421)

    def test_unicode_character_limit_matches_post_body_budget(self):
        token = self.csrf_token()
        self.assertEqual(self.post("/submit", token, message="🙂" * 2000)[0], 303)
        self.assertEqual(self.post("/submit", token, message="🙂" * 2001)[0], 400)


if __name__ == "__main__":
    unittest.main()

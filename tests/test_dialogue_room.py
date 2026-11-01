import concurrent.futures
import http.client
import os
from pathlib import Path
import re
import sqlite3
import stat
import tempfile
import threading
import unittest
from urllib.parse import urlencode

from dialogue_room.app import MessageStore, make_server, render_home, render_thread


class StoreTests(unittest.TestCase):
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
             return_token=None, origin=None):
        data = {"name": name, "message": message, "csrf": token}
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
        return re.search(r"name='csrf' value='([^']+)'", html).group(1)

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
        self.assertEqual(self.request("POST", "/submit", "x" * 5000, {
            "Content-Type": "application/x-www-form-urlencoded"})[0], 413)
        self.assertEqual(self.request("GET", "/", headers={"Host": "attacker.example"})[0], 421)


if __name__ == "__main__":
    unittest.main()

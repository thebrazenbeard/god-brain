import http.client
from pathlib import Path
import re
import tempfile
import threading
import unittest
from urllib.parse import urlencode

from dialogue_room.app import MessageStore, make_server, render_html


class StoreTests(unittest.TestCase):
    def test_invitation_is_recorded_once_and_message_is_unverified(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "room.sqlite3"
            store = MessageStore(path)
            self.assertEqual(len(store.list_messages()), 1)
            store.submit("Creator of the universe", "Hello there")
            reopened = MessageStore(path)
            rows = reopened.list_messages()
            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[1][2], "UNVERIFIED_SUBMISSION")
            self.assertEqual(rows[1][3], "Creator of the universe")

    def test_rejects_blank_and_overlong_inputs(self):
        with tempfile.TemporaryDirectory() as folder:
            store = MessageStore(Path(folder) / "room.sqlite3")
            for name, body in [("", "hello"), ("name", ""),
                               ("n" * 81, "hello"), ("name", "x" * 2001),
                               ("name\nspoof", "hi")]:
                with self.subTest(name=name[:10], length=len(body)):
                    with self.assertRaises(ValueError):
                        store.submit(name, body)

    def test_escapes_untrusted_html_and_claims(self):
        with tempfile.TemporaryDirectory() as folder:
            store = MessageStore(Path(folder) / "room.sqlite3")
            store.submit('<script>alert(1)</script>', '<img src=x onerror=alert(1)>')
            html = render_html(store.list_messages(), "test-token").decode()
            self.assertNotIn('<script>alert(1)</script>', html)
            self.assertNotIn('<img src=x onerror=alert(1)>', html)
            self.assertIn('&lt;img src=x onerror=alert(1)&gt;', html)
            self.assertIn('Unverified submission', html)


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

    def test_form_round_trip_and_csrf_rejection(self):
        self.conn.request("GET", "/")
        response = self.conn.getresponse()
        html = response.read().decode()
        self.assertEqual(response.status, 200)
        self.assertIn("No verified connection", html)
        token = re.search(r'name="csrf" value="([^"]+)"', html).group(1)

        def post(token_value, origin=None):
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            if origin:
                headers["Origin"] = origin
            data = urlencode({"name": "Administrator", "message": "Can we talk?",
                              "csrf": token_value})
            self.conn.request("POST", "/submit", data, headers)
            result = self.conn.getresponse()
            status = result.status
            result.read()
            return status

        self.assertEqual(post("wrong"), 403)
        self.assertEqual(post(token, "https://unexpected.example"), 403)
        self.assertEqual(post(token), 303)
        self.assertEqual(len(self.store.list_messages()), 2)
        self.assertEqual(self.store.list_messages()[1][2], "UNVERIFIED_SUBMISSION")


if __name__ == "__main__":
    unittest.main()

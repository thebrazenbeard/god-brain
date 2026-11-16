"""Explicit, anonymous cross-origin Pages -> real private room navigation.

Only a new-thread POST may originate at GitHub Pages. The browser follows
its 303 to the private room, which never grants Pages API read access.
"""
import http.client
import json
from pathlib import Path
import re
import tempfile
import threading
import unittest
from urllib.parse import urlencode

from dialogue_room.app import MessageStore, PublicLimits, make_server

ROOM = "https://lappy.tail86ea75.ts.net:10000"
HOST = "lappy.tail86ea75.ts.net:10000"
PAGES = "https://thebrazenbeard.github.io"
OTHER = "https://untrusted.example"


class PagesHandoffTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.store = MessageStore(Path(self.folder.name) / "inbox.sqlite3",
                                  public_limits=PublicLimits(10, 25, 10))
        self.server = make_server(self.store, 0, public_origin=ROOM)
        self.worker = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.worker.start()
        self.conn = http.client.HTTPConnection("127.0.0.1", self.server.server_port)

    def tearDown(self):
        self.conn.close()
        self.server.shutdown()
        self.server.server_close()
        self.worker.join(timeout=3)
        self.folder.cleanup()

    def request(self, method, path, body=None, headers=None):
        self.conn.request(method, path, body, {"Host": HOST, **(headers or {})})
        r = self.conn.getresponse()
        return r.status, dict(r.getheaders()), r.read().decode("utf-8")

    def ticket(self):
        status, headers, text = self.request(
            "GET", "/pages-handoff-ticket", headers={"Origin": PAGES})
        self.assertEqual(status, 200)
        self.assertEqual(headers.get("Access-Control-Allow-Origin"), PAGES)
        self.assertEqual(headers["Cache-Control"], "no-store")
        self.assertEqual(headers.get("Vary"), "Origin")
        self.assertNotIn("Access-Control-Allow-Credentials", headers)
        payload = json.loads(text)
        for name, minimum in [("csrf", 32), ("initial_token", 40), ("request_key", 24)]:
            self.assertTrue(re.fullmatch(r"[A-Za-z0-9_-]+", payload[name]))
            self.assertGreaterEqual(len(payload[name]), minimum)
        return payload

    def test_ticket_is_available_only_to_exact_pages_origin(self):
        self.ticket()
        for origin in (OTHER, "null", ROOM, PAGES + ".evil"):
            with self.subTest(origin=origin):
                status, headers, _ = self.request(
                    "GET", "/pages-handoff-ticket", headers={"Origin": origin})
                self.assertEqual(status, 403)
                self.assertNotIn("Access-Control-Allow-Origin", headers)
        self.assertEqual(self.request("GET", "/pages-handoff-ticket")[0], 403)

    def test_pages_submission_creates_private_thread_with_consent(self):
        ticket = self.ticket()
        body = urlencode({"name": "Public Visitor", "message": "Private new conversation",
                          "privacy_consent": "dialogue-privacy-v1", **ticket})
        headers = {"Origin": PAGES,
                   "Content-Type": "application/x-www-form-urlencoded"}
        code, response, _ = self.request("POST", "/submit", body, headers)
        self.assertEqual(code, 303)
        self.assertEqual(response.get("Location"), "/t/" + ticket["initial_token"])
        self.assertNotIn("Access-Control-Allow-Origin", response)
        view = self.store.thread_view(ticket["initial_token"])
        self.assertEqual(view[0][0][4], "Private new conversation")
        self.assertEqual(view[0][0][5], "held")
        self.assertNotIn("Access-Control-Allow-Origin",
                         self.request("GET", response["Location"],
                                      headers={"Origin": PAGES})[1])
        self.assertEqual(self.request("POST", "/reply", body, headers)[0], 403)
        self.assertEqual(self.request("POST", "/request-deletion", body, headers)[0], 403)
        self.assertEqual(self.request("POST", "/submit", body, headers)[0], 303)
        self.assertEqual(len(self.store.thread_messages(ticket["initial_token"])), 1)

    def test_pages_submission_rejects_missing_consent_wrong_token_and_origin(self):
        ticket = self.ticket()
        data = {"name": "Visitor", "message": "Hello", **ticket}
        headers = {"Origin": PAGES, "Content-Type": "application/x-www-form-urlencoded"}
        self.assertEqual(self.request("POST", "/submit", urlencode(data), headers)[0], 400)
        data["privacy_consent"] = "dialogue-privacy-v1"
        self.assertEqual(self.request("POST", "/submit", urlencode(
            {**data, "csrf": "invalid"}), headers)[0], 403)
        self.assertEqual(self.request("POST", "/submit", urlencode(data),
                                      {**headers, "Origin": OTHER})[0], 403)
        self.assertEqual(len(self.store.list_threads()), 0)

    def test_local_mode_does_not_enable_pages_handoff(self):
        server = make_server(MessageStore(Path(self.folder.name) / "local.sqlite3"),
                             0)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            conn = http.client.HTTPConnection("127.0.0.1", server.server_port)
            conn.request("GET", "/pages-handoff-ticket",
                         headers={"Host": f"127.0.0.1:{server.server_port}",
                                  "Origin": PAGES})
            r = conn.getresponse()
            self.assertEqual(r.status, 404)
            r.read()
            conn.close()
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=3)


if __name__ == "__main__":
    unittest.main()

"""Tailscale Funnel candidate: fail-closed origin and bounded public submissions."""

import concurrent.futures
import http.client
from pathlib import Path
import re
import secrets
import tempfile
import threading
import unittest
from urllib.parse import urlencode

from dialogue_room.app import MessageStore, PublicLimits, QuotaExceeded, make_server


ORIGIN = "https://invitation.example.ts.net:10000"
HOST = "invitation.example.ts.net:10000"


class PublicOriginTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.store = MessageStore(Path(self.tmp.name) / "room.sqlite3",
                                  public_limits=PublicLimits(4, 5, 3))
        self.server = make_server(self.store, 0, public_origin=ORIGIN)
        self.worker = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.worker.start()
        self.conn = http.client.HTTPConnection("127.0.0.1", self.server.server_port)

    def tearDown(self):
        self.conn.close()
        self.server.shutdown()
        self.server.server_close()
        self.worker.join(timeout=3)
        self.tmp.cleanup()

    def request(self, method, path, body=None, headers=None):
        headers = {"Host": HOST, **(headers or {})}
        self.conn.request(method, path, body, headers)
        result = self.conn.getresponse()
        return result.status, dict(result.getheaders()), result.read().decode()

    def test_public_origin_accepts_only_exact_tls_host_and_origin(self):
        status, _, html = self.request("GET", "/")
        self.assertEqual(status, 200)
        self.assertIn("experimental Internet-facing conversation channel", html)
        self.assertIn("no identity", html.lower())
        self.assertEqual(self.request("GET", "/", headers={"Host": "evil.example"})[0], 421)
        self.assertEqual(self.request("GET", "/", headers={"Host": "127.0.0.1"})[0], 421)
        csrf = re.search(r"name='csrf' value='([^']+)'", html).group(1)
        token = secrets.token_urlsafe(32)
        body = urlencode({"name": "Visitor", "message": "Hello", "csrf": csrf,
                          "request_key": secrets.token_urlsafe(24), "initial_token": token})
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        self.assertEqual(self.request("POST", "/submit", body, headers)[0], 403)
        self.assertEqual(self.request("POST", "/submit", body,
                                      {**headers, "Origin": "https://evil.example"})[0], 403)
        status, response_headers, _ = self.request("POST", "/submit", body,
                                                    {**headers, "Origin": ORIGIN})
        self.assertEqual(status, 303)
        self.assertEqual(response_headers["Location"], "/t/" + token)
        thread = self.request("GET", "/t/" + token)[2]
        self.assertIn(ORIGIN + "/t/" + token, thread)
        self.assertEqual(self.request("GET", "/t/" + token)[1]["Cache-Control"], "no-store")

    def test_http_rate_cap_returns_429_without_losing_old_retry_receipt(self):
        html = self.request("GET", "/")[2]
        csrf = re.search(r"name='csrf' value='([^']+)'", html).group(1)
        headers = {"Content-Type": "application/x-www-form-urlencoded", "Origin": ORIGIN}
        first_form = None
        for i in range(3):
            payload = urlencode({"name": "Visitor", "message": f"Turn {i}",
                                 "csrf": csrf, "request_key": secrets.token_urlsafe(24),
                                 "initial_token": secrets.token_urlsafe(32)})
            if i == 0:
                first_form = payload
            self.assertEqual(self.request("POST", "/submit", payload, headers)[0], 303)
        fourth_form = urlencode({"name": "Visitor", "message": "Blocked turn",
                                "csrf": csrf, "request_key": secrets.token_urlsafe(24),
                                "initial_token": secrets.token_urlsafe(32)})
        self.assertEqual(self.request("POST", "/submit", fourth_form, headers)[0], 429)
        self.assertEqual(self.request("POST", "/submit", first_form, headers)[0], 303)
        self.assertEqual(len(self.store.list_threads()), 3)

    def test_public_mode_requires_explicit_storage_limits(self):
        with tempfile.TemporaryDirectory() as folder:
            unrestricted = MessageStore(Path(folder) / "room.sqlite3")
            with self.assertRaises(ValueError):
                make_server(unrestricted, 0, public_origin=ORIGIN)

    def test_public_origin_rejects_non_https_or_non_tailscale_origin(self):
        for origin in ("http://invitation.example.ts.net:10000",
                       "https://evil.example:10000",
                       "https://invitation.example.ts.net:443",
                       "https://invitation.example.ts.net:10000/trick",
                       "https://user@invitation.example.ts.net:10000"):
            with self.subTest(origin=origin), self.assertRaises(ValueError):
                make_server(self.store, 0, public_origin=origin)


class PublicQuotaTests(unittest.TestCase):
    def test_invalid_limits_fail_closed(self):
        for values in ((0, 100, 10), (100, -1, 10), (100, 100, True)):
            with self.subTest(values=values), self.assertRaises(ValueError):
                PublicLimits(*values)

    def test_limits_reject_overflow_without_creating_or_leaking_threads(self):
        with tempfile.TemporaryDirectory() as folder:
            store = MessageStore(Path(folder) / "room.sqlite3",
                                 public_limits=PublicLimits(2, 2, 2))
            first = store.submit("Visitor", "One")
            second = store.submit("Visitor", "Two")
            with self.assertRaises(QuotaExceeded):
                store.submit("Visitor", "Three")
            self.assertEqual(len(store.list_threads()), 2)
            self.assertEqual(len(store.pending()), 2)
            self.assertEqual(len(store.thread_messages(first.token)), 1)
            self.assertEqual(len(store.thread_messages(second.token)), 1)

    def test_racing_submissions_cannot_exceed_atomic_global_cap(self):
        with tempfile.TemporaryDirectory() as folder:
            store = MessageStore(Path(folder) / "room.sqlite3",
                                 public_limits=PublicLimits(3, 3, 3))
            barrier = threading.Barrier(10)

            def attempt(i):
                barrier.wait()
                try:
                    return store.submit("Visitor", f"Turn {i}")
                except QuotaExceeded:
                    return None

            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:
                receipts = list(pool.map(attempt, range(10)))
            self.assertEqual(sum(receipt is not None for receipt in receipts), 3)
            self.assertEqual(len(store.list_threads()), 3)
            self.assertEqual(len(store.pending()), 3)


if __name__ == "__main__":
    unittest.main()

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

from dialogue_room.app import (MessageStore, PublicLimits, QuotaExceeded,
                               ThreadClosed, make_server)


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
        status, landing_headers, html = self.request("GET", "/")
        self.assertEqual(status, 200)
        self.assertEqual(landing_headers["Referrer-Policy"], "same-origin")
        self.assertIn("experimental Internet-facing conversation channel", html)
        self.assertIn("no identity", html.lower())
        self.assertEqual(self.request("GET", "/", headers={"Host": "evil.example"})[0], 421)
        self.assertEqual(self.request("GET", "/", headers={"Host": "127.0.0.1"})[0], 421)
        csrf = re.search(r"name='csrf' value='([^']+)'", html).group(1)
        token = secrets.token_urlsafe(32)
        body = urlencode({"name": "Visitor", "message": "Hello", "csrf": csrf,
                          "request_key": secrets.token_urlsafe(24), "initial_token": token,
                          "privacy_consent": "dialogue-privacy-v1"})
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        self.assertEqual(self.request("POST", "/submit", body, headers)[0], 403)
        self.assertEqual(self.request("POST", "/submit", body,
                                      {**headers, "Origin": "https://evil.example"})[0], 403)
        status, response_headers, _ = self.request("POST", "/submit", body,
                                                    {**headers, "Origin": ORIGIN})
        self.assertEqual(status, 303)
        self.assertEqual(response_headers["Location"], "/t/" + token)
        status, thread_headers, thread = self.request("GET", "/t/" + token)
        self.assertEqual(status, 200)
        self.assertEqual(thread_headers["Referrer-Policy"], "same-origin")
        self.assertIn(ORIGIN + "/t/" + token, thread)
        self.assertEqual(self.request("GET", "/t/" + token)[1]["Cache-Control"], "no-store")

    def test_public_submission_requires_versioned_consent_and_audits_acceptance(self):
        html = self.request("GET", "/")[2]
        self.assertIn("name='privacy_consent'", html)
        self.assertIn("value='dialogue-privacy-v1'", html)
        csrf = re.search(r"name='csrf' value='([^']+)'", html).group(1)
        token = secrets.token_urlsafe(32)
        payload = {"name": "Visitor", "message": "Please reply", "csrf": csrf,
                   "request_key": secrets.token_urlsafe(24), "initial_token": token}
        headers = {"Content-Type": "application/x-www-form-urlencoded", "Origin": ORIGIN}
        self.assertEqual(self.request("POST", "/submit", urlencode(payload), headers)[0], 400)
        self.assertEqual(self.request("POST", "/submit", urlencode({
            **payload, "privacy_consent": "unknown-policy"
        }), headers)[0], 400)
        self.assertEqual(len(self.store.list_threads()), 0)
        self.assertEqual(self.request("POST", "/submit", urlencode({
            **payload, "privacy_consent": "dialogue-privacy-v1"
        }), headers)[0], 303)
        thread_id = self.store.list_threads()[0][0]
        actions = [(actor, action) for _, _, actor, action, _ in
                   self.store.audit_events(thread_id)]
        self.assertIn(("UNVERIFIED_RETURN_LINK_HOLDER", "consent:dialogue-privacy-v1"), actions)
        self.assertNotIn(token, str(actions))
        # An old initial form can be reposted with a new request key; it must
        # not falsely claim a second initial consent event for this thread.
        self.assertEqual(self.request("POST", "/submit", urlencode({
            **payload, "message": "Second turn via old form",
            "request_key": secrets.token_urlsafe(24),
            "privacy_consent": "dialogue-privacy-v1",
        }), headers)[0], 303)
        actions = [row[3] for row in self.store.audit_events(thread_id)]
        self.assertEqual(actions.count("consent:dialogue-privacy-v1"), 1)

    def test_private_link_holder_can_queue_one_deletion_request_even_at_quota(self):
        html = self.request("GET", "/")[2]
        csrf = re.search(r"name='csrf' value='([^']+)'", html).group(1)
        token = secrets.token_urlsafe(32)
        headers = {"Content-Type": "application/x-www-form-urlencoded", "Origin": ORIGIN}
        first = urlencode({"name": "Visitor", "message": "A private message", "csrf": csrf,
                           "request_key": secrets.token_urlsafe(24), "initial_token": token,
                           "privacy_consent": "dialogue-privacy-v1"})
        self.assertEqual(self.request("POST", "/submit", first, headers)[0], 303)
        thread_id = self.store.list_threads()[0][0]
        for i in range(4):
            self.store.owner_reply(thread_id, f"Operator turn {i}")
        self.assertEqual(len(self.store.thread_messages(token)), 5)
        self.assertIn("action='/request-deletion'", self.request("GET", "/t/" + token)[2])
        deletion = urlencode({"return_token": token, "csrf": csrf})
        self.assertEqual(self.request("POST", "/request-deletion", deletion,
                                      {**headers, "Origin": "https://wrong.example"})[0], 403)
        self.assertEqual(self.request("POST", "/request-deletion",
                                      urlencode({"return_token": "unknown", "csrf": csrf}),
                                      headers)[0], 400)
        self.assertEqual(self.request("POST", "/request-deletion", deletion, headers)[0], 303)
        self.assertEqual(self.request("POST", "/request-deletion", deletion, headers)[0], 303)
        self.assertEqual(self.store.thread_state(token), "open")
        requests = [row for row in self.store.thread_messages(token)
                    if row[2] == "DELETION_REQUEST"]
        self.assertEqual(len(requests), 1)
        self.assertEqual(requests[0][5], "held")
        self.assertIn("delete", requests[0][4].lower())
        self.assertIn(requests[0][0], [pending[0] for pending in self.store.pending()])
        actions = [row[3] for row in self.store.audit_events(thread_id)]
        self.assertEqual(actions.count("deletion_requested"), 1)
        self.assertNotIn(token, str(self.store.audit_events(thread_id)))
        self.assertTrue(self.store.review(requests[0][0], "reviewed"))
        self.assertEqual(self.store.thread_state(token), "open")
        self.assertTrue(self.store.close_thread(thread_id, "revoked"))
        self.assertEqual(self.request("POST", "/request-deletion", deletion, headers)[0], 410)

    def test_http_rate_cap_returns_429_without_losing_old_retry_receipt(self):
        html = self.request("GET", "/")[2]
        csrf = re.search(r"name='csrf' value='([^']+)'", html).group(1)
        headers = {"Content-Type": "application/x-www-form-urlencoded", "Origin": ORIGIN}
        first_form = None
        for i in range(3):
            payload = urlencode({"name": "Visitor", "message": f"Turn {i}",
                                 "csrf": csrf, "request_key": secrets.token_urlsafe(24),
                                 "initial_token": secrets.token_urlsafe(32),
                                 "privacy_consent": "dialogue-privacy-v1"})
            if i == 0:
                first_form = payload
            self.assertEqual(self.request("POST", "/submit", payload, headers)[0], 303)
        fourth_form = urlencode({"name": "Visitor", "message": "Blocked turn",
                                "csrf": csrf, "request_key": secrets.token_urlsafe(24),
                                "initial_token": secrets.token_urlsafe(32),
                                "privacy_consent": "dialogue-privacy-v1"})
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
            first = store.submit("Visitor", "One", consent_version="dialogue-privacy-v1")
            second = store.submit("Visitor", "Two", consent_version="dialogue-privacy-v1")
            with self.assertRaises(QuotaExceeded):
                store.submit("Visitor", "Three", consent_version="dialogue-privacy-v1")
            self.assertEqual(len(store.list_threads()), 2)
            self.assertEqual(len(store.pending()), 2)
            self.assertEqual(len(store.thread_messages(first.token)), 1)
            self.assertEqual(len(store.thread_messages(second.token)), 1)

    def test_operator_deletion_reclaims_one_slot_without_reusing_old_link(self):
        with tempfile.TemporaryDirectory() as folder:
            store = MessageStore(Path(folder) / "room.sqlite3",
                                 public_limits=PublicLimits(2, 20, 20))
            first = store.submit("Visitor", "One", consent_version="dialogue-privacy-v1")
            store.submit("Visitor", "Two", consent_version="dialogue-privacy-v1")
            with self.assertRaises(QuotaExceeded):
                store.submit("Visitor", "Three", consent_version="dialogue-privacy-v1")
            self.assertTrue(store.delete_thread(first.thread_id))
            self.assertIsNone(store.thread_messages(first.token))
            with self.assertRaises(ThreadClosed):
                store.submit("Visitor", "Old link", token=first.token,
                             create_thread=True, consent_version="dialogue-privacy-v1")
            third = store.submit("Visitor", "Three", consent_version="dialogue-privacy-v1")
            self.assertIsNotNone(store.thread_messages(third.token))
            with self.assertRaises(QuotaExceeded):
                store.submit("Visitor", "Four", consent_version="dialogue-privacy-v1")

    def test_closing_and_revoking_do_not_free_thread_slots(self):
        with tempfile.TemporaryDirectory() as folder:
            store = MessageStore(Path(folder) / "room.sqlite3",
                                 public_limits=PublicLimits(2, 20, 20))
            first = store.submit("Visitor", "One", consent_version="dialogue-privacy-v1")
            second = store.submit("Visitor", "Two", consent_version="dialogue-privacy-v1")
            self.assertTrue(store.close_thread(first.thread_id, "closed"))
            self.assertTrue(store.close_thread(second.thread_id, "revoked"))
            with self.assertRaises(QuotaExceeded):
                store.submit("Visitor", "Three", consent_version="dialogue-privacy-v1")

    def test_racing_submissions_cannot_exceed_atomic_global_cap(self):
        with tempfile.TemporaryDirectory() as folder:
            store = MessageStore(Path(folder) / "room.sqlite3",
                                 public_limits=PublicLimits(3, 3, 3))
            barrier = threading.Barrier(10)

            def attempt(i):
                barrier.wait()
                try:
                    return store.submit("Visitor", f"Turn {i}",
                                        consent_version="dialogue-privacy-v1")
                except QuotaExceeded:
                    return None

            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:
                receipts = list(pool.map(attempt, range(10)))
            self.assertEqual(sum(receipt is not None for receipt in receipts), 3)
            self.assertEqual(len(store.list_threads()), 3)
            self.assertEqual(len(store.pending()), 3)


if __name__ == "__main__":
    unittest.main()

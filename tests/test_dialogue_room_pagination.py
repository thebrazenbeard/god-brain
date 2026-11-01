"""Regression contracts for bounded, private dialogue history navigation.

These intentionally exercise public store and HTTP seams. No hosted service or
provider account is involved. The local HTTP tests require loopback sockets.
"""

import http.client
from contextlib import closing
from pathlib import Path
import re
import secrets
import sqlite3
import tempfile
import threading
import unittest

from dialogue_room.app import MessageStore, make_server


class PageStoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.store = MessageStore(Path(self.tmp.name) / "private.sqlite3")

    def tearDown(self):
        self.tmp.cleanup()

    def test_thread_and_owner_history_pages_cover_every_turn(self):
        original = self.store.submit("Visitor", "turn-000")
        ids = [original.message_id]
        for index in range(1, 405):
            receipt = self.store.submit("Visitor", f"turn-{index:03d}", original.token)
            ids.append(receipt.message_id)

        # Keyset pages are bounded. A stale cursor remains useful while newer
        # messages arrive, and no old message is lost or repeated.
        seen = []
        before = None
        page_sizes = []
        for page_index in range(3):
            view = self.store.thread_view(original.token, before_id=before)
            self.assertIsNotNone(view)
            page, state, next_before = view
            self.assertEqual(state, "open")
            page_sizes.append(len(page))
            page_ids = [row[0] for row in page]
            self.assertEqual(page_ids, sorted(page_ids))
            seen.extend(page_ids)
            if page_index == 0:
                self.assertEqual(next_before, page_ids[0])
                self.store.submit("Visitor", "new-after-cursor", original.token)
            before = next_before

        self.assertEqual(page_sizes, [200, 200, 5])
        self.assertIsNone(before)
        self.assertEqual(len(seen), len(set(seen)))
        self.assertEqual(set(seen), set(ids))
        self.assertEqual(len(self.store.thread_messages(original.token)), 200)

        owner_seen = []
        before = None
        while True:
            page, before = self.store.read_thread_page(original.thread_id, before_id=before)
            self.assertLessEqual(len(page), 200)
            owner_seen.extend(row[0] for row in page)
            if before is None:
                break
        self.assertEqual(set(owner_seen), set(ids) | {max(ids) + 1})
        self.assertEqual(len(owner_seen), len(set(owner_seen)))

    def test_exact_200_and_201_message_boundaries(self):
        receipt = self.store.submit("Visitor", "turn-000")
        for index in range(1, 200):
            self.store.submit("Visitor", f"turn-{index:03d}", receipt.token)
        page, _, before = self.store.thread_view(receipt.token)
        self.assertEqual(len(page), 200)
        self.assertIsNone(before)

        self.store.submit("Visitor", "turn-200", receipt.token)
        page, _, before = self.store.thread_view(receipt.token)
        self.assertEqual(len(page), 200)
        self.assertEqual(before, page[0][0])
        older, _, no_more = self.store.thread_view(receipt.token, before_id=before)
        self.assertEqual(len(older), 1)
        self.assertIsNone(no_more)

    def test_indexes_present_after_reopening_existing_database(self):
        receipt = self.store.submit("Visitor", "Test")
        MessageStore(self.store.path)
        with closing(sqlite3.connect(self.store.path)) as db, db:
            def indexed_columns(table):
                return {
                    tuple(row[2] for row in db.execute(f"PRAGMA index_info({index[1]})"))
                    for index in db.execute(f"PRAGMA index_list({table})").fetchall()
                }
            self.assertIn(("thread_id", "id"), indexed_columns("messages"))
            self.assertIn(("speaker", "status", "id"), indexed_columns("messages"))
            self.assertIn(("thread_id", "id"), indexed_columns("moderation_events"))
        self.assertEqual(self.store.thread_view(receipt.token)[0][0][4], "Test")

    def test_pending_pages_include_items_beyond_100_and_new_arrivals(self):
        ids = [self.store.submit("Visitor", f"pending-{i}").message_id
               for i in range(112)]
        first, after = self.store.pending_page()
        self.assertEqual(len(first), 100)
        self.assertEqual([row[0] for row in first], ids[:100])
        self.assertEqual(after, ids[99])
        self.assertEqual(len(self.store.pending()), 100)

        extra = self.store.submit("Visitor", "new-pending")
        second, after2 = self.store.pending_page(after_id=after)
        self.assertEqual([row[0] for row in second], ids[100:] + [extra.message_id])
        self.assertIsNone(after2)

    def test_thread_list_pages_cover_older_threads_stably(self):
        ids = [self.store.submit("Visitor", f"thread-{i}").thread_id
               for i in range(103)]
        first, before = self.store.list_threads_page()
        self.assertEqual(len(first), 100)
        self.assertEqual([row[0] for row in first], ids[::-1][:100])
        self.assertEqual(before, ids[3])
        self.assertEqual(len(self.store.list_threads()), 100)

        new_id = self.store.submit("Visitor", "newest-after-cursor").thread_id
        second, no_more = self.store.list_threads_page(before_id=before)
        self.assertEqual([row[0] for row in second], ids[:3][::-1])
        self.assertIsNone(no_more)
        self.assertNotIn(new_id, [row[0] for row in second])

    def test_audit_pages_cover_more_than_200_actions_without_bodies(self):
        receipt = self.store.submit("Visitor", "Do not print this body")
        for index in range(205):
            self.store.owner_reply(receipt.thread_id, f"owner-response-{index}")
        first, before = self.store.audit_events_page(receipt.thread_id)
        self.assertEqual(len(first), 200)
        self.assertIsNotNone(before)
        second, no_more = self.store.audit_events_page(receipt.thread_id,
                                                        before_id=before)
        self.assertEqual(len(second), 5)
        self.assertIsNone(no_more)
        all_event_ids = [row[0] for row in first + second]
        self.assertEqual(len(set(all_event_ids)), 205)
        self.assertNotIn("owner-response", repr(first + second))
        self.assertEqual(len(self.store.audit_events(receipt.thread_id)), 200)

    def test_invalid_cursors_fail_closed_for_store_methods(self):
        receipt = self.store.submit("Visitor", "hello")
        for bad in (0, -1, "no", "1", 1.5, True, 2 ** 63):
            with self.subTest(value=repr(bad)):
                with self.assertRaises(ValueError):
                    self.store.thread_view(receipt.token, before_id=bad)
                with self.assertRaises(ValueError):
                    self.store.pending_page(after_id=bad)
                with self.assertRaises(ValueError):
                    self.store.list_threads_page(before_id=bad)
                with self.assertRaises(ValueError):
                    self.store.read_thread_page(receipt.thread_id, before_id=bad)
                with self.assertRaises(ValueError):
                    self.store.audit_events_page(receipt.thread_id, before_id=bad)

    def test_revocation_blocks_paged_reads_and_thread_isolation_remains(self):
        one = self.store.submit("Visitor", "Secret alpha")
        two = self.store.submit("Visitor", "Secret beta")
        self.store.submit("Visitor", "More alpha", one.token)
        view = self.store.thread_view(one.token, before_id=2 ** 62)
        self.assertNotIn("Secret beta", repr(view))
        self.assertIsNone(self.store.thread_view("invalid", before_id=2 ** 62))
        self.assertTrue(self.store.close_thread(one.thread_id, "revoked"))
        self.assertIsNone(self.store.thread_view(one.token, before_id=2 ** 62))
        self.assertEqual(self.store.thread_view(two.token)[0][0][4], "Secret beta")


class PageHttpTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.store = MessageStore(Path(self.tmp.name) / "private.sqlite3")
        self.server = make_server(self.store, port=0)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=3)
        self.tmp.cleanup()

    def get(self, path):
        conn = http.client.HTTPConnection("127.0.0.1", self.server.server_port)
        try:
            conn.request("GET", path)
            res = conn.getresponse()
            return res.status, dict(res.getheaders()), res.read().decode("utf-8")
        finally:
            conn.close()

    def test_private_http_history_navigation_and_bad_cursor(self):
        one = self.store.submit("Visitor", "alpha-000")
        for index in range(1, 205):
            self.store.submit("Visitor", f"alpha-{index:03d}", one.token)
        other = self.store.submit("Visitor", "Secret beta")

        status, headers, page1 = self.get(f"/t/{one.token}")
        self.assertEqual(status, 200)
        self.assertEqual(headers["Cache-Control"], "no-store")
        self.assertIn("alpha-204", page1)
        self.assertNotIn("alpha-000", page1)
        self.assertNotIn("Secret beta", page1)
        self.assertIn("Older messages", page1)
        found = re.search(rf"/t/{re.escape(one.token)}\?before=(\d+)", page1)
        self.assertIsNotNone(found)

        status, _, page2 = self.get(found.group(0))
        self.assertEqual(status, 200)
        self.assertIn("alpha-000", page2)
        self.assertNotIn("alpha-204", page2)
        self.assertNotIn("Secret beta", page2)
        self.assertNotIn("Older messages", page2)

        for bad in ("0", "-1", "+1", "1e2", "no", "1&before=2", "1&other=2",
                    "999999999999999999999999999"):
            with self.subTest(cursor=bad):
                code, _, body = self.get(f"/t/{one.token}?before={bad}")
                self.assertEqual(code, 400)
                self.assertNotIn("alpha-000", body)
                self.assertNotIn(one.token, body)

        self.assertEqual(self.get(f"/t/{other.token}?before=999999")[0], 200)
        self.assertNotIn("alpha-000", self.get(f"/t/{other.token}?before=999999")[2])
        self.assertEqual(self.get(f"/t/{secrets.token_urlsafe(32)}?before=100")[0], 404)
        self.assertIn("X-Robots-Tag", headers)
        self.assertTrue(self.store.close_thread(one.thread_id, "revoked"))
        self.assertEqual(self.get(found.group(0))[0], 404)

    def test_closed_thread_keeps_paged_history_but_no_follow_up_form(self):
        receipt = self.store.submit("Visitor", "oldest")
        for index in range(200):
            self.store.submit("Visitor", f"recent-{index}", receipt.token)
        self.assertTrue(self.store.close_thread(receipt.thread_id, "closed"))
        code, _, page = self.get(f"/t/{receipt.token}")
        self.assertEqual(code, 200)
        self.assertNotIn("action='/reply'", page)
        self.assertIn("Conversation closed", page)
        found = re.search(rf"/t/{re.escape(receipt.token)}\?before=(\d+)", page)
        self.assertIsNotNone(found)
        code, _, older = self.get(found.group(0))
        self.assertEqual(code, 200)
        self.assertIn("oldest", older)
        self.assertNotIn("action='/reply'", older)
        self.assertIn(f"http://127.0.0.1:{self.server.server_port}/t/{receipt.token}", older)


if __name__ == "__main__":
    unittest.main()

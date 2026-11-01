import tempfile
from pathlib import Path
import unittest

from dialogue_room.app import MessageStore
from dialogue_room.notifier import ALERT, notify_once


class NotifierTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "inbox.sqlite3"
        self.store = MessageStore(self.path)

    def test_recovery_cursor_and_no_duplicate_after_success(self):
        self.store.submit("a", "first")
        seen = []
        self.assertEqual(notify_once(self.path, seen.append), 1)
        self.assertEqual(seen, [ALERT])
        self.assertEqual(notify_once(self.path, seen.append), 0)
        self.store.submit("b", "second")
        self.assertEqual(notify_once(self.path, seen.append), 1)

    def test_failed_delivery_does_not_advance_cursor(self):
        self.store.submit("a", "first")
        def fail(_):
            raise OSError("offline")
        with self.assertRaises(OSError):
            notify_once(self.path, fail)
        self.assertEqual(notify_once(self.path, lambda _: None), 1)

    def test_paginates_and_never_transmits_content(self):
        for n in range(4):
            self.store.submit("secret-name", "private body " + str(n))
        sent = []
        self.assertEqual(notify_once(self.path, sent.append, batch_size=2), 2)
        self.assertEqual(notify_once(self.path, sent.append, batch_size=2), 2)
        self.assertEqual(notify_once(self.path, sent.append, batch_size=2), 0)
        self.assertEqual(sent, [ALERT, ALERT])


if __name__ == "__main__":
    unittest.main()

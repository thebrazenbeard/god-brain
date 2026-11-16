"""Contract for a clear GitHub Pages entrypoint into the separate dialogue service."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
ROOM = "https://lappy.tail86ea75.ts.net:10000/"


class DialogueEntryTests(unittest.TestCase):
    def test_homepage_has_direct_dialogue_navigation_without_stale_offline_status(self):
        html = (SITE / "index.html").read_text(encoding="utf-8")
        self.assertIn('href="./dialogue.html"', html)
        self.assertIn('href="' + ROOM + '"', html)
        self.assertNotIn("last seen offline", html.lower())
        self.assertNotIn("Last measured November 15, 2026: HTTP 502", html)
        self.assertIn("Availability can change", html)

    def test_dialogue_entry_is_responsive_accessible_and_opens_real_service(self):
        html = (SITE / "dialogue.html").read_text(encoding="utf-8")
        self.assertIn('<!doctype html>', html)
        self.assertIn('name="viewport"', html)
        self.assertIn('href="#main"', html)
        self.assertIn('id="main"', html)
        self.assertIn('<h1', html)
        self.assertIn('href="' + ROOM + '"', html)
        self.assertIn('rel="noopener noreferrer"', html)
        self.assertIn('./styles.css', html)
        self.assertIn("Private conversation", html)

    def test_static_page_does_not_impersonate_a_chat_backend(self):
        html = (SITE / "dialogue.html").read_text(encoding="utf-8")
        self.assertIn("human-reviewed", html)
        self.assertIn("separate service", html)
        self.assertIn("return link", html)
        self.assertNotIn("<iframe", html.lower())
        self.assertNotIn("<form", html.lower())
        self.assertNotIn("fetch(", html)
        self.assertIn("connect-src 'none'", html)
        self.assertIn("form-action 'none'", html)


if __name__ == "__main__":
    unittest.main()

"""A safe, useful static composer that hands off to the separate private inbox."""
from pathlib import Path
import unittest

SITE = Path(__file__).resolve().parents[1] / "site"


class PagesDialogueComposeTests(unittest.TestCase):
    def test_static_page_has_an_editable_draft_and_real_room_handoff(self):
        html = (SITE / "dialogue.html").read_text(encoding="utf-8")
        self.assertIn('id="draft-message"', html)
        self.assertIn('maxlength="2000"', html)
        self.assertIn('id="draft-count"', html)
        self.assertIn('id="copy-draft"', html)
        self.assertIn('id="draft-status"', html)
        self.assertIn('aria-live="polite"', html)
        self.assertIn('src="./dialogue.js"', html)
        self.assertIn('href="https://lappy.tail86ea75.ts.net:10000/"', html)

    def test_composer_is_in_primary_dialogue_screen_not_below_the_intro(self):
        html = (SITE / "dialogue.html").read_text(encoding="utf-8")
        start = html.index('<section class="dialogue-section"')
        hero_end = html.index("</section>", start)
        self.assertLess(html.index('id="draft-message"'), hero_end)
        self.assertLess(html.index('id="copy-draft"'), hero_end)
    def test_drafts_remain_local_until_explicitly_submitted(self):
        html = (SITE / "dialogue.html").read_text(encoding="utf-8")
        js = (SITE / "dialogue.js").read_text(encoding="utf-8")
        self.assertIn("Nothing is sent until you explicitly", html)
        self.assertIn("clipboard history", html)
        self.assertIn("browser may restore form values", html)
        self.assertIn("paste", html.lower())
        self.assertIn("human-reviewed", html)
        self.assertIn("script-src 'self'", html)
        self.assertIn("connect-src https://lappy.tail86ea75.ts.net:10000", html)
        self.assertIn("form-action https://lappy.tail86ea75.ts.net:10000", html)
        self.assertNotIn("<iframe", html)
        self.assertIn('id="dialogue-form"', html)
        self.assertIn('name="privacy_consent"', html)
        for forbidden in ("fetch(", "localStorage", "sessionStorage",
                          "XMLHttpRequest", "sendBeacon", "WebSocket"):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, js)


if __name__ == "__main__":
    unittest.main()

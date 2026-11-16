"""Direct new-conversation submission must be explicit, scoped, and consented."""
from pathlib import Path
import unittest

SITE = Path(__file__).resolve().parents[1] / "site"


class PagesSendTests(unittest.TestCase):
    def test_real_submit_form_and_consent(self):
        html = (SITE / "dialogue.html").read_text(encoding="utf-8")
        self.assertIn('id="dialogue-form"', html)
        self.assertIn('method="post"', html)
        self.assertIn('action="https://lappy.tail86ea75.ts.net:10000/submit"', html)
        self.assertIn('name="name"', html)
        self.assertIn('name="message"', html)
        self.assertIn('name="privacy_consent"', html)
        self.assertIn('value="dialogue-privacy-v1"', html)
        self.assertIn('name="csrf"', html)
        self.assertIn('name="initial_token"', html)
        self.assertIn('name="request_key"', html)
        self.assertIn('id="send-message"', html)
        self.assertIn('id="send-status"', html)
        self.assertIn('id="return-link-panel" hidden', html)
        self.assertIn('id="private-return-url"', html)
        self.assertIn('id="return-link-saved"', html)
        self.assertIn('id="copy-return-link"', html)
        self.assertIn('disabled>Prepare private link</button>', html)
        self.assertIn('src="./dialogue-submit.js"', html)

    def test_public_origin_is_limited_to_ticket_and_form_navigation(self):
        html = (SITE / "dialogue.html").read_text(encoding="utf-8")
        js = (SITE / "dialogue-submit.js").read_text(encoding="utf-8")
        target = "https://lappy.tail86ea75.ts.net:10000"
        self.assertIn("connect-src " + target, html)
        self.assertIn("form-action " + target, html)
        self.assertIn("script-src 'self'", html)
        self.assertIn('referrer" content="strict-origin-when-cross-origin"', html)
        self.assertNotIn("<iframe", html)
        self.assertNotIn("localStorage", js)
        self.assertNotIn("sessionStorage", js)
        self.assertIn("window.top !== window.self", js)
        self.assertIn('returnPanel.hidden = true', js)
        self.assertIn('saved.checked', js)
        self.assertIn('form.submit()', js)
        self.assertNotIn("XMLHttpRequest", js)
        self.assertNotIn("sendBeacon", js)
        self.assertIn('const origin = "' + target + '"', js)
        self.assertIn('origin + "/pages-handoff-ticket"', js)
        self.assertNotIn("/reply", js)
        self.assertNotIn("/request-deletion", js)
        self.assertIn("until that operator chooses to delete", html)


if __name__ == "__main__":
    unittest.main()

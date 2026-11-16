"""HTML dialogue-interface invariants for the same-origin, human-operated room."""

import unittest

from dialogue_room.app import render_home, render_thread


class DialogueInterfaceTests(unittest.TestCase):
    def test_public_entrypoint_is_responsive_accessible_and_postable(self):
        page = render_home("csrf-test", public_mode=True).decode("utf-8")
        self.assertIn('<meta name="viewport" content="width=device-width, initial-scale=1">', page)
        self.assertIn('href="#main"', page)
        self.assertIn('<main class="wrap" id="main">', page)
        self.assertIn("@media(max-width:640px)", page)
        self.assertIn("Begin a private conversation", page)
        self.assertIn("action='/submit'", page)
        self.assertIn("name='privacy_consent'", page)
        self.assertIn("name='request_key'", page)
        self.assertIn("name='initial_token'", page)
        self.assertIn("name='csrf'", page)
        self.assertNotIn("<script", page.lower())
        self.assertNotIn("<iframe", page.lower())

    def test_thread_displays_speaker_distinctions_and_escapes_messages(self):
        rows = [
            (1, "2026-11-16T00:00:00+00:00", "UNVERIFIED_SUBMISSION", "Someone",
             "<img src=x onerror=alert(1)>", "held"),
            (2, "2026-11-16T00:01:00+00:00", "PROJECT_OWNER", "",
             "Thank you; message received.", "public"),
        ]
        token = "private-test-return-token"
        page = render_thread(rows, token, "csrf-test",
                             base_url="https://example.test").decode("utf-8")
        self.assertIn("class='message message--held'", page)
        self.assertIn("class='message message--owner'", page)
        self.assertIn("&lt;img src=x onerror=alert(1)&gt;", page)
        self.assertNotIn("<img src=x onerror=alert(1)>", page)
        self.assertIn("Project owner (local operator)", page)
        self.assertIn("Unverified submission", page)
        self.assertIn("action='/reply'", page)
        self.assertIn("action='/request-deletion'", page)
        self.assertIn("https://example.test/t/" + token, page)
        self.assertIn("No response is guaranteed", page.replace("no response", "No response"))
        self.assertNotIn("<script", page.lower())

    def test_closed_thread_has_history_but_no_reply_form(self):
        page = render_thread(
            [(1, "2026-11-16", "UNVERIFIED_SUBMISSION", "Tester", "Hello", "held")],
            "private-token", "csrf", thread_state="closed",
        ).decode("utf-8")
        self.assertIn("Your conversation", page)
        self.assertIn("Conversation closed", page)
        self.assertNotIn("action='/reply'", page)
        self.assertIn("action='/request-deletion'", page)


if __name__ == "__main__":
    unittest.main()

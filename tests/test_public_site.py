"""Offline invariants for a static, public-safe God Brain web interface."""
from html.parser import HTMLParser
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
WORKFLOW = ROOT / ".github" / "workflows" / "pages.yml"

class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.links = []
        self.scripts = []
        self.headings = []
    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if "id" in data:
            self.ids.add(data["id"])
        if tag == "a":
            self.links.append(data.get("href", ""))
        if tag == "script":
            self.scripts.append(data.get("src", ""))
        if tag in {"h1", "h2", "h3"}:
            self.headings.append(tag)

class PublicSiteTests(unittest.TestCase):
    def test_site_contains_a_public_entrypoint_and_local_assets(self):
        html = (SITE / "index.html").read_text(encoding="utf-8")
        parser = PageParser()
        parser.feed(html)
        self.assertIn("h1", parser.headings)
        self.assertTrue({"main", "architecture", "bench", "dialogue"} <= parser.ids)
        self.assertIn("./app.js", parser.scripts)
        self.assertIn("./styles.css", html)
        self.assertTrue((SITE / "styles.css").is_file())
        self.assertTrue((SITE / "app.js").is_file())
        self.assertIn("Content-Security-Policy", html)
    def test_dialogue_link_is_separate_from_static_site(self):
        html = (SITE / "index.html").read_text(encoding="utf-8")
        self.assertIn("https://lappy.tail86ea75.ts.net:10000/", html)
        self.assertIn("not receive or store messages", html)
        self.assertIn("No respondent", html)
        self.assertIn("OBSERVATION", html)
    def test_private_recordings_have_no_implicit_network_or_storage(self):
        js = (SITE / "app.js").read_text(encoding="utf-8")
        for banned in ("innerHTML", "localStorage", "sessionStorage",
                       "fetch(", "XMLHttpRequest", "sendBeacon", "eval("):
            with self.subTest(banned=banned):
                self.assertNotIn(banned, js)
        self.assertIn("textContent", js)
        self.assertIn("createObjectURL", js)
    def test_pages_deployment_is_scoped_to_main_and_uses_pinned_actions(self):
        yaml = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("branches: [main]", yaml)
        self.assertIn("if: github.event_name != 'pull_request'", yaml)
        self.assertIn("pages: write", yaml)
        self.assertIn("id-token: write", yaml)
        self.assertIn("persist-credentials: false", yaml)
        self.assertIn("path: ./site", yaml)
        self.assertNotIn("uses: actions/checkout@v", yaml)
    def test_no_external_resources_in_our_html(self):
        html = (SITE / "index.html").read_text(encoding="utf-8")
        self.assertNotIn("https://fonts.", html)
        self.assertNotIn("<iframe", html)
        self.assertNotIn("<form action=\"http", html)
        self.assertIn("connect-src 'none'", html)

if __name__ == "__main__":
    unittest.main()

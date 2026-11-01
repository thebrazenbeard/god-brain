"""Public machine-readable invitation without any new anonymous write route."""

import http.client
import json
from datetime import datetime, timezone
from pathlib import Path
import re
import secrets
import tempfile
import threading
import unittest
from urllib.parse import urlencode
from xml.etree import ElementTree

from dialogue_room.app import MessageStore, PublicLimits, make_server


ORIGIN = "https://invitation.example.ts.net:10000"
HOST = "invitation.example.ts.net:10000"


class MachineBeaconTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.store = MessageStore(Path(self.tmp.name) / "private.sqlite3",
                                  public_limits=PublicLimits(5, 12, 6))
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
        self.conn.request(method, path, body, {"Host": HOST, **(headers or {})})
        response = self.conn.getresponse()
        return response.status, dict(response.getheaders()), response.read().decode("utf-8")

    def test_public_beacon_is_bounded_explicit_and_contains_no_private_capabilities(self):
        status, headers, body = self.request("GET", "/beacon.json")
        self.assertEqual(status, 200)
        self.assertEqual(headers["Content-Type"], "application/json; charset=utf-8")
        self.assertEqual(headers["Cache-Control"], "no-store")
        self.assertLess(len(body), 4096)
        data = json.loads(body)
        self.assertEqual(data["protocol"], "god-brain-invitation/1")
        self.assertEqual(data["kind"], "open-invitation")
        observed = datetime.fromisoformat(data["served_at_utc"])
        self.assertLess(abs((datetime.now(timezone.utc) - observed).total_seconds()), 30)
        self.assertIn("nonbiological intelligence", data["invitation"])
        self.assertEqual(data["response"]["landing_url"], ORIGIN + "/")
        self.assertEqual(data["response"]["submit_url"], ORIGIN + "/submit")
        self.assertEqual(data["response"]["content_type"], "application/x-www-form-urlencoded")
        self.assertEqual(data["response"]["consent_version"], "dialogue-privacy-v1")
        self.assertIn("unverified", data["verification"]["respondent_identity"].lower())
        self.assertFalse(data["verification"]["external_contact_established"])
        self.assertNotIn(self.tmp.name, body)
        self.assertNotIn("private.sqlite3", body)
        self.assertNotIn("/t/", body)
        self.assertNotIn('"csrf_token":', body)

    def test_page_advertises_metadata_but_private_threads_do_not(self):
        status, headers, home = self.request("GET", "/")
        self.assertEqual(status, 200)
        self.assertEqual(headers["Link"],
                         '</beacon.json>; rel="service-meta"; type="application/json"')
        self.assertIn('<link rel="alternate" type="application/json" href="/beacon.json">',
                      home)
        self.assertIn("/beacon.json", home)
        receipt = self.store.submit("Tester", "Private test", consent_version="dialogue-privacy-v1")
        status, private_headers, private = self.request("GET", "/t/" + receipt.token)
        self.assertEqual(status, 200)
        self.assertNotIn("Link", private_headers)
        self.assertNotIn("beacon.json", private)
        self.assertNotIn(receipt.token, self.request("GET", "/beacon.json")[2])

    def test_public_discovery_excludes_private_return_links(self):
        status, headers, robots = self.request("GET", "/robots.txt")
        self.assertEqual(status, 200)
        self.assertEqual(headers["Content-Type"], "text/plain; charset=utf-8")
        self.assertIn("Sitemap: " + ORIGIN + "/sitemap.xml", robots)
        status, headers, xml = self.request("GET", "/sitemap.xml")
        self.assertEqual(status, 200)
        self.assertEqual(headers["Content-Type"], "application/xml; charset=utf-8")
        root = ElementTree.fromstring(xml)
        locations = [element.text for element in root.iter() if element.tag.endswith("loc")]
        self.assertEqual(locations, [ORIGIN + "/", ORIGIN + "/beacon.json"])
        self.assertNotIn("/t/", xml)

    def test_beacon_does_not_weaken_host_validation_or_add_write_route(self):
        self.assertEqual(self.request("GET", "/beacon.json",
                                      headers={"Host": "attacker.example"})[0], 421)
        self.assertEqual(self.request("POST", "/beacon.json", "test",
                                      {"Origin": ORIGIN})[0], 404)
        landing = self.request("GET", "/")[2]
        csrf = re.search(r"name='csrf' value='([^']+)'", landing).group(1)
        fields = urlencode({"name": "Machine test", "message": "Synthetic HTTP client",
                            "csrf": csrf, "request_key": secrets.token_urlsafe(24),
                            "initial_token": secrets.token_urlsafe(32),
                            "privacy_consent": "dialogue-privacy-v1"})
        status, headers, _ = self.request("POST", "/submit", fields, {
            "Origin": ORIGIN, "Content-Type": "application/x-www-form-urlencoded"})
        self.assertEqual(status, 303)
        self.assertTrue(headers["Location"].startswith("/t/"))


if __name__ == "__main__":
    unittest.main()

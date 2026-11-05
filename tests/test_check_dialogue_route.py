"""Negative-first checks for fail-closed God Brain runtime route identity."""

from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import socket
import sys
import threading
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from check_dialogue_route import (  # noqa: E402
    classify_beacon, main, probe, validate_origin,
)


ORIGIN = "https://sample.ts.net:10000"
HOST = "sample.ts.net:10000"


def beacon(*, origin=ORIGIN, protocol="god-brain-invitation/1"):
    return json.dumps({
        "protocol": protocol,
        "kind": "open-invitation",
        "served_at_utc": datetime.now(timezone.utc).isoformat(),
        "response": {"landing_url": origin + "/",
                     "submit_url": origin + "/submit"},
    }).encode()


class SyntheticHandler(BaseHTTPRequestHandler):
    status = 200
    body = beacon()
    content_type = "application/json"
    host_seen = None

    def do_GET(self):
        type(self).host_seen = self.headers.get("Host")
        self.send_response(type(self).status)
        self.send_header("Content-Type", type(self).content_type)
        self.send_header("Content-Length", str(len(type(self).body)))
        self.end_headers()
        self.wfile.write(type(self).body)

    def log_message(self, *args):
        pass


class RouteProbeTests(unittest.TestCase):
    def test_valid_contract_and_wrong_service_even_at_http_200(self):
        self.assertEqual(classify_beacon(200, "application/json", beacon(), ORIGIN),
                         "healthy")
        self.assertEqual(classify_beacon(200, "text/html", b"<html>OK</html>", ORIGIN),
                         "not_json_content_type")
        self.assertEqual(classify_beacon(200, "application/json",
                                         beacon(protocol="other/1"), ORIGIN),
                         "wrong_service")
        self.assertEqual(classify_beacon(200, "application/json",
                                         beacon(origin="https://other.ts.net:10000"), ORIGIN),
                         "wrong_origin")
        self.assertEqual(classify_beacon(502, "text/html", b"Bad Gateway", ORIGIN),
                         "http_502")
        self.assertEqual(classify_beacon(200, "application/json", b"", ORIGIN),
                         "invalid_beacon")

    def test_invalid_stale_or_oversize_beacon(self):
        data = json.loads(beacon())
        data["served_at_utc"] = "2000-01-01T00:00:00+00:00"
        self.assertEqual(classify_beacon(200, "application/json",
                                         json.dumps(data).encode(), ORIGIN),
                         "stale_beacon")
        self.assertEqual(classify_beacon(200, "application/json", b"x" * 8193,
                                         ORIGIN), "oversize_beacon")

    def test_rejects_non_funnel_or_private_credentials(self):
        for value in ("http://sample.ts.net:10000", "https://sample.ts.net",
                      "https://sample.ts.net:443", "https://sample.ts.net:10000/path",
                      "https://user:secret@sample.ts.net:10000"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                validate_origin(value)

    def test_actual_loopback_request_uses_public_host_and_fails_closed(self):
        class Handler(SyntheticHandler):
            pass

        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        worker = threading.Thread(target=server.serve_forever, daemon=True)
        worker.start()
        try:
            self.assertEqual(probe(ORIGIN, backend_port=server.server_port),
                             "healthy")
            self.assertEqual(Handler.host_seen, HOST)
            Handler.body = b"<html>temporary preview</html>"
            Handler.content_type = "text/html"
            self.assertEqual(probe(ORIGIN, backend_port=server.server_port),
                             "not_json_content_type")
            Handler.status = 502
            self.assertEqual(probe(ORIGIN, backend_port=server.server_port),
                             "http_502")
        finally:
            server.shutdown()
            server.server_close()
            worker.join(timeout=3)

        self.assertEqual(probe(ORIGIN, backend_port=server.server_port,
                               timeout=0.3), "connection_failed")

    def test_empty_reply_from_unhealthy_listener_fails(self):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.bind(("127.0.0.1", 0))
        listener.listen(1)
        port = listener.getsockname()[1]

        def drop_request():
            try:
                connection, _ = listener.accept()
                with connection:
                    connection.recv(4096)
                    # Accepting TCP alone is never evidence of a working route.
            finally:
                listener.close()

        worker = threading.Thread(target=drop_request, daemon=True)
        worker.start()
        try:
            self.assertEqual(probe(ORIGIN, backend_port=port, timeout=1),
                             "connection_failed")
        finally:
            worker.join(timeout=3)


if __name__ == "__main__":
    unittest.main()

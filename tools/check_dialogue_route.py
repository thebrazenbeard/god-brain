"""Read-only health/contract probe for the optional God Brain Funnel service.

This tool never starts a service, edits routing, or touches the dialogue database.
It distinguishes a listening *other* process from the expected dialogue service;
an HTTP 200 from an arbitrary web server is not a healthy God Brain route.
This is a semantic fingerprint, not cryptographic authentication of a server.

Usage::

    python tools/check_dialogue_route.py \
        --public-origin https://example.ts.net:10000 --backend-port 18765 \
        --check-funnel

All failures exit nonzero. The result contains classifications, not HTTP bodies,
visitor information, paths, credentials, or response headers.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import http.client
import json
from urllib.parse import urlsplit


MAX_BEACON_BYTES = 8192
EXPECTED_PROTOCOL = "god-brain-invitation/1"
EXPECTED_KIND = "open-invitation"


def validate_origin(value: str) -> str:
    """Accept only the dedicated HTTPS Funnel origin allowed by the app."""
    parsed = urlsplit(value)
    if (parsed.scheme != "https" or parsed.port != 10000
            or not parsed.hostname or not parsed.hostname.endswith(".ts.net")
            or parsed.username is not None or parsed.password is not None
            or parsed.path or parsed.query or parsed.fragment):
        raise ValueError("expected exact https://<host>.ts.net:10000 origin")
    return value


def classify_beacon(status: int, content_type: str, body: bytes,
                    origin: str, *, max_age_seconds: int = 300) -> str:
    """Return 'healthy' or a bounded failure code, never a response body."""
    if status != 200:
        return f"http_{status}"
    if content_type.split(";", 1)[0].strip().lower() != "application/json":
        return "not_json_content_type"
    if len(body) > MAX_BEACON_BYTES:
        return "oversize_beacon"
    try:
        payload = json.loads(body)
        response = payload["response"]
        timestamp = datetime.fromisoformat(payload["served_at_utc"])
    except (ValueError, TypeError, KeyError, UnicodeDecodeError):
        return "invalid_beacon"
    if not isinstance(payload, dict) or not isinstance(response, dict):
        return "invalid_beacon"
    if (payload.get("protocol") != EXPECTED_PROTOCOL
            or payload.get("kind") != EXPECTED_KIND):
        return "wrong_service"
    if (response.get("landing_url") != origin + "/"
            or response.get("submit_url") != origin + "/submit"):
        return "wrong_origin"
    if timestamp.tzinfo is None:
        return "invalid_timestamp"
    age = abs((datetime.now(timezone.utc) - timestamp).total_seconds())
    if age > max_age_seconds:
        return "stale_beacon"
    return "healthy"


def probe(origin: str, *, backend_port: int | None,
          timeout: float = 3.0) -> str:
    """Check the local port or the actual public Funnel without following redirects."""
    parsed = urlsplit(validate_origin(origin))
    if backend_port is None:
        connection = http.client.HTTPSConnection(parsed.hostname, parsed.port,
                                                 timeout=timeout)
    else:
        if not 1 <= backend_port <= 65535:
            raise ValueError("backend port out of range")
        connection = http.client.HTTPConnection("127.0.0.1", backend_port,
                                                timeout=timeout)
    try:
        connection.request("GET", "/beacon.json", headers={
            "Host": parsed.netloc,
            "Accept": "application/json",
            "Cache-Control": "no-store",
        })
        response = connection.getresponse()
        body = response.read(MAX_BEACON_BYTES + 1)
        return classify_beacon(response.status,
                               response.getheader("Content-Type", ""), body,
                               origin)
    except (OSError, http.client.HTTPException, TimeoutError):
        return "connection_failed"
    finally:
        connection.close()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--public-origin", required=True)
    parser.add_argument("--backend-port", type=int, default=18765)
    parser.add_argument("--check-funnel", action="store_true")
    parser.add_argument("--timeout", type=float, default=3.0)
    args = parser.parse_args(argv)
    try:
        validate_origin(args.public_origin)
        if not 1 <= args.backend_port <= 65535 or not 0 < args.timeout <= 30:
            raise ValueError("port or timeout out of range")
    except ValueError as exc:
        parser.error(str(exc))

    result = {"backend": probe(args.public_origin,
                                backend_port=args.backend_port,
                                timeout=args.timeout)}
    if args.check_funnel:
        result["funnel"] = probe(args.public_origin, backend_port=None,
                                 timeout=args.timeout)
    print(json.dumps(result, sort_keys=True))
    return 0 if all(value == "healthy" for value in result.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())

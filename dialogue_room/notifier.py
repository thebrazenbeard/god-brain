"""Optional local-only inbox notifier; no public endpoint or message contents.

Run independently from the dialogue server. A crash may duplicate an alert, but
never advances the durable cursor before an alert provider accepts the request.
"""

import argparse
from contextlib import closing
from pathlib import Path
import sqlite3
import time
from urllib.request import Request, urlopen


ALERT = b"New unverified God Brain submission. Check the private inbox on Lappy."


def notify_once(db_path: Path, publish, *, batch_size: int = 5000) -> int:
    """Notify for committed inbound messages; return count covered by this pass.

    A monotonic cursor makes notification restart-safe. One aggregated alert per
    batch avoids leaking visitor metadata or creating one push per submission.
    """
    with closing(sqlite3.connect(db_path, timeout=10)) as db:
        with db:
            db.execute("CREATE TABLE IF NOT EXISTS notification_state ("
                       "key TEXT PRIMARY KEY, last_id INTEGER NOT NULL)")
            db.execute("INSERT OR IGNORE INTO notification_state VALUES ('inbound',0)")
        cursor = db.execute("SELECT last_id FROM notification_state WHERE key='inbound'").fetchone()[0]
        rows = db.execute(
            "SELECT id FROM messages WHERE id>? AND speaker='UNVERIFIED_SUBMISSION' "
            "ORDER BY id LIMIT ?", (cursor, batch_size)
        ).fetchall()
        if not rows:
            return 0
        # Do not hold a SQLite writer lock during an outbound network request.
        # Publication can duplicate after an ambiguous timeout or process crash.
        publish(ALERT)
        with db:
            db.execute("UPDATE notification_state SET last_id=? WHERE key='inbound'",
                       (rows[-1][0],))
        return len(rows)


def publish_ntfy(topic: str, payload: bytes) -> None:
    # Topic contains no sender data. Its random value is a bearer-like secret.
    req = Request("https://ntfy.sh/" + topic, data=payload, method="POST",
                  headers={"Title": "God Brain inbox", "Priority": "default"})
    with urlopen(req, timeout=12) as response:
        if response.status not in (200, 201, 202):
            raise RuntimeError("Push provider did not accept notification")


def main() -> None:
    parser = argparse.ArgumentParser(description="God Brain local-only inbox alerts")
    parser.add_argument("--db", type=Path, required=True)
    parser.add_argument("--topic-file", type=Path, required=True,
                        help="Private file containing only the unguessable ntfy topic")
    parser.add_argument("--interval", type=int, default=60)
    parser.add_argument("--once", action="store_true")
    args = parser.parse_args()
    if args.interval < 60:
        parser.error("Interval must be at least 60 seconds to limit unsolicited push volume")
    topic = args.topic_file.read_text(encoding="ascii").strip()
    import re
    if not re.fullmatch(r"[A-Za-z0-9_-]{32,128}", topic):
        parser.error("Topic must be a high-entropy token, 32-128 URL-safe characters")
    while True:
        try:
            notify_once(args.db, lambda msg: publish_ntfy(topic, msg))
        except (OSError, sqlite3.Error, RuntimeError) as exc:
            print(f"Notification retry needed: {type(exc).__name__}", flush=True)
        if args.once:
            return
        time.sleep(args.interval)


if __name__ == "__main__":
    main()

# God Brain Dialogue Room — local-only reference prototype

This is an ordinary, persistent conversation room that can display an open invitation and accept replies in a browser. It **does not** establish a connection to any hypothetical external creator or administrator. Anybody can claim an identity; every submitted message is visibly and durably classified as **unverified**.

The purpose is to test a potential conversation *interface*: an invitation, a message, a follow-up, and a durable record that does not promote a claimed speaker identity to truth.

## Run locally

From the repository root with Python 3.12+:

```bash
python3 dialogue_room/app.py --db ./dialogue_room.sqlite3 --port 8765
```

Open `http://127.0.0.1:8765` on the same machine. Stop with Ctrl-C. The database file contains messages and may contain personal information; keep it private and back it up or remove it only deliberately. It is intentionally ignored from source control when integrated into the repository.

Tests:

```bash
python3 -m unittest discover -s tests -p 'test_dialogue_room.py' -v
```

## Trust and deployment boundary

- The server binds **only to loopback**; there is no public deployment, external inbox, or identity verification.
- The opening invitation is stored once. Replies are preserved in SQLite with a claimed display name but are always tagged `UNVERIFIED_SUBMISSION`.
- Untrusted HTML is escaped. Inputs are length bounded, and the form uses a per-process token and origin check.
- The current UI is a simple chronological conversation; it does not authenticate Patrick or any alleged respondent, and it is not a production security boundary.
- No network messages are sent to an external being, and the app does not use an AI model to invent a reply.
- Public operation would need a separate approved design for accounts, consent, privacy, spam/abuse controls, moderation, backups, operator access, secure transport, and independently reviewed deployment.

**Claim ceiling:** A working local two-way messaging prototype, not a creator contact system or a scientifically verified communication channel.

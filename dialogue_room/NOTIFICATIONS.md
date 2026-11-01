# Optional inbox notifications (candidate, not deployed)

This separate worker polls the existing local SQLite database; it does not
expose a new port, modify the public dialogue form, or send visitor content.

It can publish a **generic** alert to an ntfy.sh topic. Unreserved ntfy.sh
topics are public, so this is a convenience signal, **not** an authenticated
private inbox. Use an independently generated random topic with at least
32 URL-safe characters, and never publish its value in the repository, command
line, logs or screenshots. The worker reads it from a private local file.

On Lappy, after the owner installs/subscribes to the ntfy Android app and
approves the third-party notification metadata disclosure, create a private
topic file in the already protected GodBrainDialogue data directory. Confirm
the file's Windows ACLs before starting the worker. Do not use the public
beacon URL as a topic.

```powershell
$data = Join-Path $env:LOCALAPPDATA 'GodBrainDialogue'
$code = Join-Path $data 'code'
py "$code\dialogue_room\notifier.py" --db "$data\dialogue.sqlite3" --topic-file "$data\ntfy-topic.txt"
```

This foreground command is a *manual trial*, not an unattended installation.
A dedicated boot-time Windows task and one real Android notification test are
still required before claiming continuous alert delivery. The existing S4U
web-server task is not an interactive Windows desktop notification session.

The cursor is stored in `notification_state` in SQLite and advances only
after ntfy accepts an alert. A crash or ambiguous timeout may duplicate a
generic notification. Messages are never deleted or marked reviewed by the
worker. One batch per minute caps normal emissions to 60 per hour; provider
limits, outages and mobile delivery remain best-effort. The first run may
notify for historical messages; it does not erase them.

**Privacy:** The provider can observe that a notification was posted and its
topic/time. Do not send message bodies, claimed sender names, thread IDs,
return tokens, or other private conversation data. Do not interpret an alert
as verification of the sender's claimed identity.

-- Two tiny tables. No triggers, no FTS, nothing fancy.
CREATE TABLE IF NOT EXISTS emails (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  origin      TEXT NOT NULL,          -- e.g., 'manual'
  sender      TEXT NOT NULL,          -- e.g., 'Alice <alice@acme.com>'
  received_at TEXT NOT NULL,          -- ISO8601, e.g., '2025-11-02T16:00:00Z'
  subject     TEXT NOT NULL,
  content     TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS calendar (
  id        INTEGER PRIMARY KEY AUTOINCREMENT,
  title     TEXT NOT NULL,
  start_ts  TEXT NOT NULL,            -- ISO8601
  end_ts    TEXT NOT NULL,            -- ISO8601
  attendees TEXT                      -- comma-separated names/emails
);

import sqlite3
from datetime import datetime, timedelta

cx = sqlite3.connect("agno.db")

# --- 15 emails ---
rows = []
base = datetime(2025, 11, 2, 16, 0, 0)  # any baseline you want
for i in range(1, 16):
    rows.append((
        "manual",
        f"User{i} <user{i}@example.com>",
        (base + timedelta(minutes=i)).strftime("%Y-%m-%dT%H:%M:%SZ"),
        f"Sample subject {i}",
        f"Simple content body for message {i} with a name like Dana or Chris #{i}."
    ))

cx.executemany(
    "INSERT INTO emails(origin, sender, received_at, subject, content) VALUES (?,?,?,?,?)",
    rows
)

# --- 3 calendar events for the next week ---
now = datetime(2025, 11, 2, 16, 0, 0)
events = [
    ("Standup", (now + timedelta(days=1, hours=2)), 30, "Dana, Chris"),
    ("Client call", (now + timedelta(days=3, hours=1)), 45, "Alex <alex@client.com>"),
    ("Interview", (now + timedelta(days=5, hours=4)), 30, "Dana, Chris"),
]
cal_rows = []
for title, start_dt, minutes, attendees in events:
    end_dt = start_dt + timedelta(minutes=minutes)
    cal_rows.append((
        title,
        start_dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
        end_dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
        attendees
    ))

cx.executemany(
    "INSERT INTO calendar(title, start_ts, end_ts, attendees) VALUES (?,?,?,?)",
    cal_rows
)

cx.commit()
cx.close()
print("Seeded: 15 emails, 3 events.")

import os
import sqlite3
from datetime import datetime, timedelta
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.db.sqlite import SqliteDb

DATABASE_PATH = os.getenv("DATABASE_PATH", "agno.db")


def get_upcoming_events(days: int = 7) -> str:
    """
    Retrieves upcoming calendar events for the next N days.

    Args:
        days: Number of days to look ahead (default: 7)

    Returns:
        Formatted string with upcoming events
    """
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        now = datetime.now()
        end_date = now + timedelta(days=days)

        cursor.execute("""
            SELECT id, title, start_ts, end_ts, attendees
            FROM calendar
            WHERE start_ts >= ? AND start_ts <= ?
            ORDER BY start_ts ASC
        """, (now.strftime("%Y-%m-%dT%H:%M:%SZ"), end_date.strftime("%Y-%m-%dT%H:%M:%SZ")))

        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return f"No events scheduled for the next {days} days."

        result = []
        for row in rows:
            event_id, title, start_ts, end_ts, attendees = row
            result.append(f"ID: {event_id}\nTitle: {title}\nStart: {start_ts}\nEnd: {end_ts}\nAttendees: {attendees}\n")

        return "\n---\n".join(result)

    except Exception as e:
        return f"Error retrieving upcoming events: {str(e)}"


def add_calendar_event(title: str, start_ts: str, end_ts: str, attendees: str = "") -> str:
    """
    Adds a new event to the calendar.

    Args:
        title: Event title
        start_ts: Start timestamp in ISO8601 format (e.g., '2025-11-03T14:00:00Z')
        end_ts: End timestamp in ISO8601 format
        attendees: Comma-separated list of attendees (optional)

    Returns:
        Confirmation message with event ID
    """
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO calendar (title, start_ts, end_ts, attendees)
            VALUES (?, ?, ?, ?)
        """, (title, start_ts, end_ts, attendees))

        event_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return f"Event '{title}' added successfully with ID: {event_id}"

    except Exception as e:
        return f"Error adding event: {str(e)}"


def get_events_by_attendee(attendee_name: str) -> str:
    """
    Retrieves events where a specific person is an attendee.

    Args:
        attendee_name: Name or email of the attendee

    Returns:
        Formatted string with events for that attendee
    """
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, title, start_ts, end_ts, attendees
            FROM calendar
            WHERE attendees LIKE ?
            ORDER BY start_ts ASC
        """, (f"%{attendee_name}%",))

        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return f"No events found with attendee '{attendee_name}'."

        result = []
        for row in rows:
            event_id, title, start_ts, end_ts, attendees = row
            result.append(f"ID: {event_id}\nTitle: {title}\nStart: {start_ts}\nEnd: {end_ts}\nAttendees: {attendees}\n")

        return "\n---\n".join(result)

    except Exception as e:
        return f"Error retrieving events by attendee: {str(e)}"


def get_all_events() -> str:
    """
    Retrieves all calendar events from the database.

    Returns:
        Formatted string with all events
    """
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, title, start_ts, end_ts, attendees
            FROM calendar
            ORDER BY start_ts ASC
        """)

        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return "No events found in the calendar."

        result = []
        for row in rows:
            event_id, title, start_ts, end_ts, attendees = row
            result.append(f"ID: {event_id}\nTitle: {title}\nStart: {start_ts}\nEnd: {end_ts}\nAttendees: {attendees}\n")

        return "\n---\n".join(result)

    except Exception as e:
        return f"Error retrieving all events: {str(e)}"


CalendarAgent = Agent(
    name="Calendar Agent",
    model=OpenAIChat(id="gpt-4o"),
    role="Manage calendar events, add new events, and list upcoming schedule",
    db=SqliteDb(db_file=DATABASE_PATH),
    tools=[get_upcoming_events, add_calendar_event, get_events_by_attendee, get_all_events],
    instructions=[
        "Manage the calendar database including adding, retrieving, and organizing events.",
        "Help users find events by attendee, date range, or title.",
        "Provide clear summaries of upcoming schedules and commitments.",
        "When adding events, ensure timestamps are in ISO8601 format.",
    ],
    add_history_to_context=True,
    markdown=True,
)

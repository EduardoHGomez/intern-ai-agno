import os
import sqlite3
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.db.sqlite import SqliteDb

DATABASE_PATH = os.getenv("DATABASE_PATH", "agno.db")


def get_recent_emails(limit: int = 10) -> str:
    # Returns a String based list of emails
    # such that it can be parsed easily from the frontend
    """
    Retrieves the most recent emails from the database.
    Args: limit: Maximum number of emails to retrieve (default: 10)

    """
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, sender, received_at, subject, content
            FROM emails
            ORDER BY received_at DESC
            LIMIT ?
        """, (limit,))

        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return "No emails found in the database."

        result = []
        for row in rows:
            email_id, sender, received_at, subject, content = row
            result.append(f"ID: {email_id}\nFrom: {sender}\nReceived: {received_at}\nSubject: {subject}\nContent: {content}\n")

        return "\n---\n".join(result)

    except Exception as e:
        return f"Error retrieving emails: {str(e)}"


def search_emails(keyword: str) -> str:
    # Searches emails by keyword in subject or content.
    """
    Args: keyword: Keyword to search for
    Returns: Formatted string with matching emails
    """
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, sender, received_at, subject, content
            FROM emails
            WHERE subject LIKE ? OR content LIKE ?
            ORDER BY received_at DESC
        """, (f"%{keyword}%", f"%{keyword}%"))

        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return f"No emails found containing '{keyword}'."

        result = []
        for row in rows:
            email_id, sender, received_at, subject, content = row
            result.append(f"ID: {email_id}\nFrom: {sender}\nReceived: {received_at}\nSubject: {subject}\nContent: {content}\n")

        return "\n---\n".join(result)

    except Exception as e:
        return f"Error searching emails: {str(e)}"


def get_emails_by_sender(sender_name: str) -> str:
    # Retrieves emails from a specific sender.
    """
    Args: sender_name: Name or email of the sender
    Returns: Formatted string with emails from that sender
    """
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, sender, received_at, subject, content
            FROM emails
            WHERE sender LIKE ?
            ORDER BY received_at DESC
        """, (f"%{sender_name}%",))

        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return f"No emails found from '{sender_name}'."

        result = []
        for row in rows:
            email_id, sender, received_at, subject, content = row
            result.append(f"ID: {email_id}\nFrom: {sender}\nReceived: {received_at}\nSubject: {subject}\nContent: {content}\n")

        return "\n---\n".join(result)

    except Exception as e:
        return f"Error retrieving emails by sender: {str(e)}"


EmailAgent = Agent(
    name="Email Agent",
    model=OpenAIChat(id="gpt-4o"),
    role="Read and summarize emails from the database, extract names and relevant information",
    db=SqliteDb(db_file=DATABASE_PATH),
    tools=[get_recent_emails, search_emails, get_emails_by_sender],
    instructions=[
        "Search and retrieve emails from the SQLite database.",
        "Summarize email content and extract key information like names, dates, and topics.",
        "Help users find specific emails based on sender, subject, or keywords.",
        "Provide clear, concise summaries of email threads and conversations.",
    ],
    add_history_to_context=True,
    markdown=True,
)

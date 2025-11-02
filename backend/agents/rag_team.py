import os
from agno.team.team import Team
from agno.models.openai import OpenAIChat
from agno.db.sqlite import SqliteDb
from .email_agent import EmailAgent
from .calendar_agent import CalendarAgent

DATABASE_PATH = os.getenv("DATABASE_PATH", "agno.db")

RAGTeam = Team(
    name="Personal Assistant Team",
    model=OpenAIChat(id="gpt-4o"),
    members=[EmailAgent, CalendarAgent],
    db=SqliteDb(db_file=DATABASE_PATH),
    instructions=[
        "Work together to help users manage their emails and calendar.",
        "Email Agent: Retrieve and summarize emails, extract key information and names.",
        "Calendar Agent: Manage calendar events, show upcoming schedule, and add new events.",
        "Coordinate between agents when tasks involve both emails and calendar (e.g., scheduling meetings based on email requests).",
        "Provide comprehensive, well-structured responses that address the user's complete request.",
    ],
    add_history_to_context=True,
    store_history_messages=True,
    num_history_runs=3,
    markdown=True,
)

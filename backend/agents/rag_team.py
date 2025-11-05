import os
from agno.team.team import Team
from agno.models.openai import OpenAIChat
from agno.db.sqlite import SqliteDb
from .email_agent import EmailAgent
from .calendar_agent import CalendarAgent
from .exa_agent import ExaAgent

DATABASE_PATH = os.getenv("DATABASE_PATH", "agno.db")

RAGTeam = Team(
    name="Personal Assistant Team",
    model=OpenAIChat(id="gpt-4o"),
    members=[EmailAgent, CalendarAgent, ExaAgent],
    db=SqliteDb(db_file=DATABASE_PATH),
    instructions=[
        "Work together to help users manage their emails, calendar, and information needs.",
        "**Email Agent**: Retrieve and summarize emails, extract key information and names.",
        "**Calendar Agent**: Manage calendar events, show upcoming schedule, and add new events.",
        "**Exa Search Agent**: Handle ALL web searches, research queries, news lookups, documentation searches, and content retrieval requests.",
        "Use Exa Search Agent when the user asks to:",
        "  - Search for information, news, articles, or documentation",
        "  - Find content about specific topics or companies",
        "  - Get current information about events, people, or technologies",
        "  - Retrieve content from specific URLs",
        "  - Research a topic or question",
        "Coordinate between agents when tasks involve multiple domains.",
        "Provide comprehensive, well-structured responses with sources when using Exa.",
        "Always include source URLs when information comes from web searches.",
    ],
    add_history_to_context=True,
    store_history_messages=True,
    num_history_runs=3,
    markdown=True,
)
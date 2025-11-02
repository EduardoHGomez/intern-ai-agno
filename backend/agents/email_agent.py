import os
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.db.sqlite import SqliteDb

DATABASE_PATH = os.getenv("DATABASE_PATH", "agno.db")

EmailAgent = Agent(
    name="Scheduler Agent",
    model=OpenAIChat(
        id="gpt-4o",
    ),
    db=SqliteDb(db_file=DATABASE_PATH),
    add_history_to_context=True,
    markdown=True,
)

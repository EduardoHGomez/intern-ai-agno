import os
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.db.sqlite import SqliteDb

DATABASE_PATH = os.getenv("DATABASE_PATH", "agno.db")

InterAgent = Agent(
    name="Intern AI Agent",
    model=OpenAIChat(
        id="gpt-4",
    ),
    db=SqliteDb(db_file=DATABASE_PATH),
    add_history_to_context=True,
    markdown=True,
    store_history_messages=True,
    num_history_runs=3,
)

import os
from agno.db.sqlite import SqliteDb
from .rag_team import RAGTeam

DATABASE_PATH = os.getenv("DATABASE_PATH", "agno.db")

# InternAgent now uses the RAGTeam for coordinated email and calendar management
InternAgent = RAGTeam

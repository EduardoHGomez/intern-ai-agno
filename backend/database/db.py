import os
from agno.db.sqlite import SqliteDb

# Configs for DB
def get_database() -> SqliteDb:
    database_path = os.getenv("DATABASE_PATH", "agno.db")
    return SqliteDb(db_file=database_path)

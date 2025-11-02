# Agent Backend - Intern AI

A production-ready FastAPI backend powered by Agno's agentic framework. Uses distributed RAG architecture with specialized agents for email management and calendar coordination, backed by SQLite for local knowledge storage.

## What It Does

This backend implements a multi-agent RAG system that:
- **EmailAgent**: Retrieves, searches, and summarizes emails from SQLite
- **CalendarAgent**: Manages calendar events and schedules
- **RAGTeam**: Coordinates both agents to handle complex queries

Built with Agno's agent framework, it maintains conversation history, supports session management, and provides a clean REST API for the frontend.

## Tech Stack

- **FastAPI** - Modern Python web framework
- **Agno** - Agentic AI framework with team coordination
- **OpenAI GPT-4o** - LLM for agent intelligence
- **SQLite** - Lightweight database for emails, calendar, and chat history
- **Docker** - Containerization for easy deployment
- **Uvicorn** - ASGI server

## Prerequisites

- Python 3.12+
- OpenAI API key
- Docker (optional, for containerized deployment)

## Quick Start

### Option 1: Local Development (Recommended for Development)

1. **Clone and navigate to backend:**
   ```
   cd backend
   ```

2. **Create virtual environment:**
   ```
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```
   cp .env.example .env
   ```

   Edit `.env` and add your API keys:
   ```env
   OPENAI_API_KEY=sk-proj-your-key-here
   FRONTEND_URL=http://localhost:3000
   DATABASE_PATH=agno.db
   ```

5. **Create database schema:**
   ```
   sqlite3 agno.db < tools/test.sql
   ```

6. **Seed the database with sample data:**
   ```
   python tools/seed_db.py
   ```

   This creates:
   - 15 sample emails from various senders
   - 3 upcoming calendar events

7. **Start the server:**
   ```
   uvicorn main:app --reload --port 8000
   ```

   Or Using uvicorn FastAPI
   ```
   fastapi dev main.py
   ```

8. **Verify it's running:**
   - API: [http://localhost:8000](http://localhost:8000)
   - Docs: [http://localhost:8000/docs](http://localhost:8000/docs)
   - Health: [http://localhost:8000/health](http://localhost:8000/health)

### Option 2: Docker (Recommended for Production)

1. **Set up environment:**
   ```
   cp .env.example .env
   # Edit .env with your API keys
   ```

2. **Build and run with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

3. **Initialize database (first time only):**
   ```bash
   # Create schema
   docker-compose exec app sqlite3 agno.db < tools/test.sql

   # Seed data
   docker-compose exec app python tools/seed_db.py
   ```

The API will be available at [http://localhost:8000](http://localhost:8000)

### Option 3: Docker without Compose

1. **Build the image:**
   ```bash
   docker build -t agent-backend .
   ```

2. **Run the container:**
   ```bash
   docker run -d -p 8000:8000 \
     -e OPENAI_API_KEY=your-key-here \
     -e FRONTEND_URL=http://localhost:3000 \
     -v $(pwd)/agno.db:/app/agno.db \
     --name agent-backend \
     agent-backend
   ```

## Environment Variables

Create a `.env` file with the following variables:

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `OPENAI_API_KEY` | **Yes** | OpenAI API key for GPT-4o | `sk-proj-...` |
| `FRONTEND_URL` | No | Frontend CORS origin | `http://localhost:3000` |
| `DATABASE_PATH` | No | SQLite database file path | `agno.db` (default) |

### Getting an OpenAI API Key

1. Go to [platform.openai.com](https://platform.openai.com/)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new secret key
5. Copy and add to your `.env` file

**Note:** You need billing set up and credits in your OpenAI account.

## Project Structure

```
backend/
├── agents/
│   ├── email_agent.py       # EmailAgent with SQLite tools
│   ├── calendar_agent.py    # CalendarAgent with event management
│   ├── rag_team.py          # Team coordinator for both agents
│   ├── intern_agent.py      # Main agent export (uses RAGTeam)
│   └── __init__.py
├── routers/
│   ├── chat.py              # Chat endpoints (/api/chat, /api/sessions)
│   ├── health.py            # Health check endpoint
│   └── __init__.py
├── database/
│   ├── db.py                # Database utilities (if needed)
│   └── __init__.py
├── tools/
│   ├── test.sql             # Database schema
│   └── seed_db.py           # Sample data seeder
├── main.py                  # FastAPI application entry point
├── requirements.txt         # Python dependencies
├── Dockerfile               # Docker image definition
├── docker-compose.yml       # Docker Compose configuration
├── .env                     # Environment variables (create from .env.example)
├── .env.example             # Environment template
└── agno.db                  # SQLite database (auto-created)
```

## API Endpoints

### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-11-02T16:00:00Z"
}
```

### Send Chat Message
```http
POST /api/chat
```

**Request:**
```json
{
  "message": "Show me my recent emails",
  "session_id": "123e4567-e89b-12d3-a456-426614174000",
  "stream": false
}
```

**Response:**
```json
{
  "session_id": "123e4567-e89b-12d3-a456-426614174000",
  "response": "Here are your most recent emails:\n\n1. **From:** User15..."
}
```

**Streaming Mode:**
Set `"stream": true` to receive Server-Sent Events (SSE) for real-time responses.

### Get Session Messages
```http
GET /api/sessions/{session_id}/messages
```

**Response:**
```json
{
  "messages": [
    {
      "role": "user",
      "content": "Show me my emails"
    },
    {
      "role": "assistant",
      "content": "Here are your emails..."
    }
  ]
}
```

## Agent System Architecture

### RAGTeam (InternAgent)
The main coordinator that delegates tasks to specialized agents.

**Configuration:**
- Model: GPT-4o
- Maintains 3 runs of conversation history
- Stores all messages in SQLite

### EmailAgent
Specialized agent for email operations.

**Tools:**
- `get_recent_emails(limit)` - Fetch latest emails
- `search_emails(keyword)` - Search by keyword in subject/content
- `get_emails_by_sender(sender_name)` - Filter by sender

**Example queries:**
- "Show me my latest emails"
- "Find emails from Dana"
- "Search emails about 'meeting'"

### CalendarAgent
Specialized agent for calendar management.

**Tools:**
- `get_upcoming_events(days)` - Get events for next N days
- `add_calendar_event(title, start_ts, end_ts, attendees)` - Create new event
- `get_events_by_attendee(attendee_name)` - Find events by participant
- `get_all_events()` - List all events

**Example queries:**
- "What's on my calendar this week?"
- "Show me events with Chris"
- "Add a meeting tomorrow at 2pm"

## Database Schema

### emails table
```sql
CREATE TABLE emails (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  origin      TEXT NOT NULL,          -- 'manual', 'gmail', etc.
  sender      TEXT NOT NULL,          -- 'Name <email@domain.com>'
  received_at TEXT NOT NULL,          -- ISO8601 timestamp
  subject     TEXT NOT NULL,
  content     TEXT NOT NULL
);
```

### calendar table
```sql
CREATE TABLE calendar (
  id        INTEGER PRIMARY KEY AUTOINCREMENT,
  title     TEXT NOT NULL,
  start_ts  TEXT NOT NULL,            -- ISO8601 timestamp
  end_ts    TEXT NOT NULL,            -- ISO8601 timestamp
  attendees TEXT                      -- Comma-separated
);
```

### Agno-managed tables
Agno automatically creates additional tables for:
- Agent runs and session history
- Tool call logs
- Message storage

## Database Management

### Resetting the Database

```bash
# Delete existing database
rm agno.db

# Recreate schema
sqlite3 agno.db < tools/test.sql

# Reseed with sample data
python tools/seed_db.py
```

### Viewing Database Contents

```bash
# Open SQLite shell
sqlite3 agno.db

# List all tables
.tables

# View emails
SELECT * FROM emails;

# View calendar events
SELECT * FROM calendar;

# Exit
.quit
```

### Custom Seed Data

Edit `tools/seed_db.py` to add your own sample data:

```python
rows.append((
    "manual",
    "Alice <alice@example.com>",
    "2025-11-03T10:00:00Z",
    "Project Update",
    "Here's the latest on the project..."
))
```

## Production Deployment

### Docker Production Build

```bash
# Build for production
docker build --platform linux/amd64 -t yourusername/agent-backend:latest .

# Push to registry
docker push yourusername/agent-backend:latest

# Deploy on server
docker pull yourusername/agent-backend:latest
docker run -d -p 8000:8000 \
  -e OPENAI_API_KEY=your-key \
  -v /data/agno.db:/app/agno.db \
  --restart unless-stopped \
  yourusername/agent-backend:latest
```

### Environment Considerations

1. **API Keys**: Use secrets management (AWS Secrets Manager, etc.)
2. **Database**: Consider PostgreSQL for multi-user production
3. **CORS**: Update `FRONTEND_URL` to your production domain
4. **Monitoring**: Add logging, error tracking (Sentry), metrics
5. **Rate Limiting**: Implement rate limits for API endpoints
6. **Authentication**: Add user auth before production deployment

## Development

### Running Tests

```bash
# Install dev dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest
```

### Linting

```bash
# Install linters
pip install ruff black

# Format code
black .

# Lint
ruff check .
```

### Adding a New Agent

1. Create agent file in `agents/`:
```python
from agno.agent import Agent
from agno.models.openai import OpenAIChat

def my_tool(param: str) -> str:
    """Tool description"""
    return f"Result: {param}"

MyAgent = Agent(
    name="My Agent",
    model=OpenAIChat(id="gpt-4o"),
    tools=[my_tool],
    role="Agent role description",
    instructions=["Instruction 1", "Instruction 2"],
)
```

2. Add to team in `agents/rag_team.py`
3. Export in `agents/__init__.py`
4. Register in `main.py` AgentOS

## Troubleshooting

### "Module not found" errors
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### "Table does not exist" errors
```bash
# Create database schema
sqlite3 agno.db < tools/test.sql
```

### "Invalid API key" errors
- Check `.env` file exists in backend directory
- Verify `OPENAI_API_KEY` is correct
- Ensure no extra spaces or quotes in `.env`

### Port 8000 already in use
```bash
# Use different port
uvicorn main:app --reload --port 8001

# Or kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

### Docker container won't start
```bash
# Check logs
docker logs agent-backend

# Rebuild from scratch
docker-compose down -v
docker-compose up --build
```

## Performance Notes

- **SQLite**: Suitable for single-user/demo. For production with concurrent users, migrate to PostgreSQL
- **Agno History**: Currently stores 3 runs of history. Adjust `num_history_runs` in agents for longer/shorter memory
- **Response Time**: Typical response: 2-5 seconds (depends on OpenAI API latency and agent complexity)

## Security Considerations

⚠️ **Before Production:**
1. Add authentication middleware
2. Implement rate limiting
3. Validate all user inputs
4. Use environment-based secrets management
5. Enable HTTPS
6. Add request/response logging
7. Implement proper error handling (don't leak stack traces)

## License

MIT

## Support

For issues or questions:
1. Check API docs at `/docs`
2. Review logs: `docker-compose logs -f`
3. Verify `.env` configuration
4. Check Agno documentation: [agno.com](https://agno.com)

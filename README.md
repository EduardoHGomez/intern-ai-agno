# Agent - RAG-based Email & Calendar Assistant

A full-stack AI assistant with multi-agent RAG architecture. Chat with specialized agents that manage emails and calendar events, powered by Agno + FastAPI backend and Next.js frontend.

## Quick Start

### Prerequisites
- Python 3.12+
- Node.js 18+
- OpenAI API key

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Add your OPENAI_API_KEY to .env

# Initialize database
sqlite3 agno.db < tools/test.sql
python tools/seed_db.py

# Start server
uvicorn main:app --reload --port 8000
```

**Backend runs at:** [http://localhost:8000](http://localhost:8000)

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

**Frontend runs at:** [http://localhost:3000](http://localhost:3000)

## Docker Setup (Alternative)

```bash
# Backend
cd backend
cp .env.example .env  # Add your API keys
docker-compose up --build

# Initialize DB (first time)
docker-compose exec app sqlite3 agno.db < tools/test.sql
docker-compose exec app python tools/seed_db.py

# Frontend
cd frontend
npm install
npm run dev
```

## Architecture

### Backend (FastAPI + Agno)
- **RAGTeam**: Coordinates specialized agents
- **EmailAgent**: Query and search emails from SQLite
- **CalendarAgent**: Manage calendar events
- **SQLite**: Stores emails, calendar, chat history

**Key Files:**
- `backend/agents/` - Agent definitions and tools
- `backend/routers/chat.py` - API endpoints
- `backend/tools/` - DB schema and seed data

### Frontend (Next.js 15 + React 19)
- Modern chat interface with markdown rendering
- Session management with localStorage
- Real-time messaging with optional streaming

**Key Files:**
- `frontend/src/app/chat/[session_id]/page.tsx` - Chat UI
- `frontend/src/lib/sessions.ts` - Session management

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/api/chat` | POST | Send message, get AI response |
| `/api/sessions/{id}/messages` | GET | Retrieve chat history |

## Environment Variables

### Backend `.env`
```env
OPENAI_API_KEY=sk-proj-your-key-here
FRONTEND_URL=http://localhost:3000
DATABASE_PATH=agno.db
```

### Frontend
No environment variables required (API URL is hardcoded for simplicity).

## Example Queries

- "Show me my recent emails"
- "Find emails from Dana"
- "What's on my calendar this week?"
- "Show me events with Chris"
- "Add a meeting tomorrow at 2pm with the team"

## Database Schema

**emails**
```sql
id, origin, sender, received_at, subject, content
```

**calendar**
```sql
id, title, start_ts, end_ts, attendees
```

Agno auto-creates tables for agent runs, messages, and tool calls.

## Tech Stack

**Backend:**
- FastAPI, Agno, OpenAI GPT-4o, SQLite, Docker

**Frontend:**
- Next.js 15, React 19, TypeScript, Tailwind CSS v4, shadcn/ui, react-markdown

## Project Structure

```
agent/
├── backend/
│   ├── agents/           # EmailAgent, CalendarAgent, RAGTeam
│   ├── routers/          # API endpoints
│   ├── tools/            # DB schema & seed script
│   ├── main.py           # FastAPI app
│   ├── requirements.txt
│   └── Dockerfile
└── frontend/
    ├── src/
    │   ├── app/          # Next.js pages
    │   ├── components/   # UI components
    │   └── lib/          # Utils & session management
    └── package.json
```

## Production Deployment

### Backend
```bash
docker build -t agent-backend .
docker run -d -p 8000:8000 \
  -e OPENAI_API_KEY=your-key \
  -v /data/agno.db:/app/agno.db \
  agent-backend
```

### Frontend
```bash
npm run build
npm start  # or deploy to Vercel
```

## Security Notes

⚠️ **Before production:**
- Add authentication
- Implement rate limiting
- Use secrets manager for API keys
- Enable HTTPS
- Update CORS origins

## Troubleshooting

**"Module not found"**
```bash
cd backend && pip install -r requirements.txt
cd frontend && npm install
```

**"Table does not exist"**
```bash
sqlite3 agno.db < tools/test.sql
python tools/seed_db.py
```

**Port already in use**
```bash
# Backend
lsof -ti:8000 | xargs kill -9

# Frontend
lsof -ti:3000 | xargs kill -9
```

## Documentation

- **Backend Details:** [backend/README.md](backend/README.md)
- **Frontend Details:** [frontend/README.md](frontend/README.md)
- **API Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **Agno Framework:** [agno.com](https://agno.com)

## License

MIT
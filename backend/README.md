# Intern AI - Backend

This is the backend used to deploy the Agent OS on the backend.
For this project, you can configure your agents in the folder [Agents](/agents)

## Installation and Setup

### Option 1: Docker (Recommended)

1. Create `.env` file:
```bash
cp .env.example .env
# Edit .env and add your API keys
```

2. Run with Docker Compose:
```bash
docker-compose up
```

The server will be available at: `http://localhost:8000`

### Option 2: Local Development

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  
# On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file:
```bash
cp .env.example .env
# Add your API keys
```

4. Start the FastAPI server:
```bash
uvicorn main:app --reload --port 8000
```

The server will be available at: `http://localhost:8000`

## How to run
```bash
fastapi run main.py
```

## How to run in Production

### Docker Deployment

Push to `main` branch to auto-deploy:
```bash
git push origin main
```

Manual deployment:
```bash
# Build for production
docker build --platform linux/amd64 -t yourusername/agno-app:latest .
docker push yourusername/agno-app:latest

# On server
docker pull yourusername/agno-app:latest
docker run -d -p 8000:8000 \
  -e OPENAI_API_KEY=your-key \
  --restart unless-stopped \
  yourusername/agno-app:latest
```

## Endpoints

- `GET /health` - Health check endpoint
- `POST /api/chat` - Chat endpoint (expects `{"message": "your text"}`)

## Testing with Agno

The `/api/chat` endpoint currently echoes your message back. Replace the logic in `main.py` at the `chat()` function with your Agno implementation.
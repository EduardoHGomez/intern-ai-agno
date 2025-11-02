# Intern AI - Backend

This is the backend used to deploy the Agent OS on the backend.

## Installation and Setup
1. Create a virtual environment (recommended):
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```
pip install -r requirements.txt
```

3. Start the FastAPI server:
```
uvicorn main:app --reload --port 8000
```

The server will be available at: `http://localhost:8000`

## How to run
```
fastapi run main.py
```

## How to run in Production
For any ASGI Server
```
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Endpoints

- `GET /health` - Health check endpoint
- `POST /api/chat` - Chat endpoint (expects `{"message": "your text"}`)

## Testing with Agno

The `/api/chat` endpoint currently echoes your message back. Replace the logic in `main.py` at the `chat()` function with your Agno implementation.

## API Documentation

Once running, view the auto-generated API docs at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

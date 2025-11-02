"""
Main FastAPI application integrated with Agno AgentOS.

This application demonstrates how to:
1. Create an Agno Agent with OpenAI
2. Integrate a custom FastAPI app with AgentOS
3. Expose custom endpoints alongside AgentOS routes
"""

import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from agno.os import AgentOS

# Load environment variables from .env file
load_dotenv()

# ============================================================================
# Configuration
# ============================================================================

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is required")

DATABASE_PATH = "agno.db"
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")


# ============================================================================
# Agent Setup
# ============================================================================

# Create the Agno Agent with OpenAI
chat_agent = Agent(
    name="Chat mio",
    model=OpenAIChat(
        id="gpt-4o",  # Using gpt-4o as in your original agno_agent.py
    ),
    # SQLite database for storing conversation history and agent state
    db=SqliteDb(db_file=DATABASE_PATH),
    # Include previous conversation history in the context
    # This allows the agent to maintain context across multiple requests
    add_history_to_context=True,
    # Format responses in markdown
    markdown=True,
    # Optional: Add tools here if needed
    # tools=[DuckDuckGoTools()],
    store_history_messages=True,
    num_history_runs=3,

)


chat_agent2 = Agent(
    name="Chat 2 we",
    model=OpenAIChat(
        id="gpt-4o",  # Using gpt-4o as in your original agno_agent.py
    ),
    # SQLite database for storing conversation history and agent state
    db=SqliteDb(db_file=DATABASE_PATH),
    # Include previous conversation history in the context
    # This allows the agent to maintain context across multiple requests
    add_history_to_context=True,
    # Format responses in markdown
    markdown=True,
    # Optional: Add tools here if needed
    # tools=[DuckDuckGoTools()],
)

# ============================================================================
# Custom FastAPI App
# ============================================================================

# Create your custom FastAPI application
app = FastAPI(
    title="Agno Chat API",
    description="FastAPI application integrated with Agno AgentOS",
    version="1.0.0",
)

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# Custom Routes
# ============================================================================

@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify the service is running.

    Returns:
        dict: Service status
    """
    return {"status": "healthy", "service": "agno-chat-api"}


@app.get("/api/sessions/{session_id}/messages")
async def get_session_messages(session_id: str):
    """
    Get all messages for a specific session.

    This endpoint retrieves the conversation history for a session from Agno's database.
    Messages are returned in chronological order (oldest first).

    Args:
        session_id: The session UUID

    Returns:
        Dict with 'messages' array containing {role, content} objects

    Raises:
        HTTPException: If there's an error retrieving messages
    """
    try:
        # Get all messages for this session using Agno's built-in method
        messages = chat_agent.get_messages_for_session(session_id=session_id)

        # Convert Agno messages to simple {role, content} format
        formatted_messages = []
        for msg in messages:
            role = msg.role if hasattr(msg, 'role') else 'assistant'
            content = msg.content if hasattr(msg, 'content') else str(msg)

            # Only include user and assistant messages (skip system messages)
            if role in ['user', 'assistant']:
                formatted_messages.append({
                    "role": role,
                    "content": content
                })

        return {"messages": formatted_messages}

    except Exception as e:
        print(f"Error retrieving session messages: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while retrieving session messages"
        )


@app.post("/api/chat")
async def chat(payload: dict = Body(...)):
    """
    Chat endpoint that uses the Agno agent to process messages.

    This endpoint:
    1. Receives a user message and session_id (UUID v4 generated by frontend)
    2. Passes it to the Agno agent with session persistence
    3. Returns the agent's response and session_id

    The agent maintains conversation history in the database keyed by session_id,
    so it can reference previous messages in the conversation.

    NOTE: session_id is generated on the frontend (crypto.randomUUID()) for simplicity.
    This ensures the session_id is unguessable (UUID v4) while avoiding the need for
    server-side session creation logic. The frontend creates the session_id and sends
    it with the first message.

    Args:
        payload: Dict with 'message' (str) and 'session_id' (str, UUID v4)

    Returns:
        Dict with 'session_id' and 'response'

    Raises:
        HTTPException: If there's an error processing the request
    """
    try:
        message = payload.get("message")
        session_id = payload.get("session_id")

        if not message:
            raise HTTPException(status_code=400, detail="message is required")

        # Use the agent to generate a response
        # The agent will use the OpenAI model and maintain conversation history
        # Note: message is a positional argument, session_id is keyword
        run = chat_agent.run(message, session_id=session_id)

        # Extract the text content from the agent's response
        text = getattr(run, "content", None) or getattr(run, "output_text", None) or str(run)

        return {"session_id": run.session_id, "response": text}

    except HTTPException:
        raise
    except Exception as e:
        # Log the error and return a user-friendly message
        print(f"Error processing chat request: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing your request"
        )


# ============================================================================
# AgentOS Integration
# ============================================================================

# Create the AgentOS instance with your custom FastAPI app
# This combines your custom routes with AgentOS's built-in endpoints
agent_os = AgentOS(
    description="Chat API with Agno AgentOS",
    agents=[chat_agent, chat_agent2],
    base_app=app,  # Pass your custom FastAPI app
)

# Get the combined FastAPI application
# This app includes:
# - Your custom routes (/health, /api/chat)
# - AgentOS routes for agent management, sessions, monitoring, etc.
app = agent_os.get_app()


# ============================================================================
# Entry Point
# ============================================================================

if __name__ == "__main__":
    """
    Run the AgentOS application.

    The AgentOS will be available at:
    - http://localhost:8000

    You can view the API documentation at:
    - http://localhost:8000/docs (Swagger UI)
    - http://localhost:8000/redoc (ReDoc)

    To run this application:
    1. Make sure you have all dependencies installed
    2. Set OPENAI_API_KEY in your .env file
    3. Run: fastapi dev main.py
    """
    agent_os.serve(app="main:app", reload=True)

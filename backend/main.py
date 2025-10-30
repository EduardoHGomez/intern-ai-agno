"""
Main FastAPI application integrated with Agno AgentOS.

This application demonstrates how to:
1. Create an Agno Agent with OpenAI
2. Integrate a custom FastAPI app with AgentOS
3. Expose custom endpoints alongside AgentOS routes
"""

import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
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
# Request/Response Models
# ============================================================================

class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    response: str


# ============================================================================
# Agent Setup
# ============================================================================

# Create the Agno Agent with OpenAI
chat_agent = Agent(
    name="Chat Agent",
    model=OpenAIChat(
        id="gpt-4o",  # Using gpt-4o as in your original agno_agent.py
        api_key=OPENAI_API_KEY,
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
    allow_origins=[FRONTEND_URL],
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


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat endpoint that uses the Agno agent to process messages.

    This endpoint:
    1. Receives a user message
    2. Passes it to the Agno agent
    3. Returns the agent's response

    The agent maintains conversation history in the database,
    so it can reference previous messages in the conversation.

    Args:
        request: ChatRequest containing the user's message

    Returns:
        ChatResponse: The agent's response

    Raises:
        HTTPException: If there's an error processing the request
    """
    try:
        user_message = request.message

        # Use the agent to generate a response
        # The agent will use the OpenAI model and maintain conversation history
        response = chat_agent.run(user_message)

        # Extract the text content from the agent's response
        bot_response = response.content if hasattr(response, 'content') else str(response)

        return ChatResponse(response=bot_response)

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
    agents=[chat_agent],
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

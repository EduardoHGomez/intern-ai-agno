import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from agno.os import AgentOS

from agents import InternAgent, EmailAgent, CalendarAgent
from routers import health_router, chat_router

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Agno Chat API",
    description="FastAPI application integrated with Agno AgentOS",
    version="1.0.0",
)

# Configure CORS - Updated
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Routers ----------
app.include_router(health_router)
app.include_router(chat_router)

# Create AgentOS with individual agents (InternAgent is a Team used directly in routers)
agent_os = AgentOS(
    description="Chat API with Agno AgentOS",
    agents=[EmailAgent, CalendarAgent],
    base_app=app,
)

# Get the combined app (includes AgentOS routes)
app = agent_os.get_app()

if __name__ == "__main__":
    agent_os.serve(app="main:app", reload=True)

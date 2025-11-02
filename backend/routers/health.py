import uuid
from fastapi import APIRouter

router = APIRouter(tags=["health"])

# Generate a unique ID for this instance
INSTANCE_ID = str(uuid.uuid4())

@router.get("/health")
async def health_check():
    return {
        "name": "AgentOS API",
        "description": "Chat API with Agno AgentOS",
        "id": INSTANCE_ID,
        "version": "1.0.0"
    }

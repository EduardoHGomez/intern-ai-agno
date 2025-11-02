from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check():
    """
    Health check endpoint to verify the service is running.

    Returns:
        dict: Service status
    """
    return {"status": "healthy", "service": "agno-chat-api"}

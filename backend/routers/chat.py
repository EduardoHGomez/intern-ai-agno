# Endpoint for the chats

from datetime import datetime
from fastapi import APIRouter, HTTPException, Body
from agents import InternAgent

router = APIRouter(prefix="/api", tags=["chat"])

@router.get("/sessions/{session_id}/messages")
async def get_session_messages(session_id: str):
    # Gets all messages given a session id
    """
    Args: session_id: The session UUID
    Returns: Dict with 'messages' array containing {role, content} objects
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] GET /api/sessions/{session_id}/messages")

    try:
        # Using Agno's internal service
        messages = InternAgent.get_messages_for_session(session_id=session_id)

        # Conversion role or assitant para solo tener cualquiera de los dos
        formatted_messages = []
        for msg in messages:
            role = msg.role if hasattr(msg, 'role') else 'assistant'
            content = msg.content if hasattr(msg, 'content') else str(msg)

            if role in ['user', 'assistant']:
                formatted_messages.append({
                    "role": role,
                    "content": content
                })

        print(f"[{timestamp}] GET /api/sessions/{session_id}/messages - {len(formatted_messages)} messages")
        return {"messages": formatted_messages}

    except Exception as e:
        print(f"[{timestamp}] GET /api/sessions/{session_id}/messages - Error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while retrieving session messages"
        )


@router.post("/chat")
async def chat(payload: dict = Body(...)):
    # Endpoint para un chat sencillo
    # NOTE: The agent maintains conversation history in the database keyed by session_id,
    # so it can reference previous messages in the conversation.

    """
    Args: payload: Dict with 'message' (str) and 'session_id' (str, UUID v4)

    Returns: Dict with 'session_id' and 'response'

    Raises: HTTPException: If there's an error processing the request
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        message = payload.get("message")
        session_id = payload.get("session_id")

        print(f"[{timestamp}] POST /api/chat - Payload: {{'message': '{message[:50]}...', 'session_id': '{session_id}'}}")

        if not message:
            raise HTTPException(status_code=400, detail="message is required")

        # Run without a session_id is stateless, that's why I used the session_id to retrieve the context
        run = InternAgent.run(message, session_id=session_id)

        # Extract the text content from the agent's response
        text = getattr(run, "content", None) or getattr(run, "output_text", None) or str(run)

        print(f"[{timestamp}] POST /api/chat - Response: {{'session_id': '{run.session_id}', 'response_length': {len(text)}}}")
        return {"session_id": run.session_id, "response": text}

    except HTTPException:
        raise
    except Exception as e:
        print(f"[{timestamp}] POST /api/chat - Error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing your request"
        )

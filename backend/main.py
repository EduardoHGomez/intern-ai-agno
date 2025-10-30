from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response models
class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}


# Chat endpoint
@app.post("/api/chat")
async def chat(request: ChatRequest):
    # TODO: Replace this with your Agno implementation
    # For now, just echo the message back
    user_message = request.message
    bot_response = f"Echo: {user_message}"

    return ChatResponse(response=bot_response)

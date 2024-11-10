from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from typing import Optional, Dict, List

from chat_model import ChatModel
from config import HOST, PORT

app = FastAPI(title="LLama 3.2 Chatbot API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize chat model
chat_model = ChatModel()

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    history: List[Dict]
    error: Optional[str] = None

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        # Generate response
        result = await chat_model.generate_response(request.message)
        
        if result["error"]:
            raise HTTPException(status_code=500, detail=result["error"])
        
        # Get conversation history
        history = chat_model.get_conversation_history()
        
        return ChatResponse(
            response=result["response"],
            history=history,
            error=None
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST, port=PORT, reload=False) 
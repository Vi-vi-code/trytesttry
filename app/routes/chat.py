from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services import groq_service, supabase_service

router = APIRouter()

# 定義了 API 的「輸入」與「輸出」格式
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat endpoint that:
    1. Fetches relevant data from Supabase
    2. Passes data as context to Groq
    3. Returns Groq's response
    """
    try:
        # Fetch context data from Supabase
        data = supabase_service.fetch_data(limit=3)
        context = str(data) if data else ""

        # Get response from Groq with the context
        response = groq_service.get_completion(
            prompt=request.message,
            context=context
        )

        return ChatResponse(response=response)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

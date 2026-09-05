from fastapi import APIRouter, HTTPException

from agent.agent import EcommerceSupportAgent
from database.models import ChatRequest, ChatResponse

router = APIRouter(prefix="/api", tags=["chat"])
agent = EcommerceSupportAgent()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    try:
        result = await agent.handle_message(request.customer_id, request.message)
        return ChatResponse(**result)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Support agent is unavailable: {exc}") from exc

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    customer_id: str = Field(..., min_length=1, max_length=40)
    message: str = Field(..., min_length=1, max_length=1000)


class ChatResponse(BaseModel):
    response: str
    tool_used: Optional[str] = None
    conversation_id: str
    products: list[dict[str, Any]] = Field(default_factory=list)


class ReturnRequest(BaseModel):
    order_id: str = Field(..., min_length=1, max_length=40)
    reason: str = Field(..., min_length=3, max_length=500)


class ReturnResponse(BaseModel):
    return_id: str
    order_id: str
    customer_id: str
    reason: str
    status: str
    created_at: datetime

from fastapi import APIRouter, HTTPException

from database.models import ReturnRequest
from tools.order_tools import get_order_status
from tools.return_tools import create_return_request

router = APIRouter(prefix="/api", tags=["orders"])


@router.get("/orders/{order_id}")
def order_status(order_id: str):
    result = get_order_status(order_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@router.post("/returns")
def create_return(request: ReturnRequest):
    result = create_return_request(request.order_id, request.reason)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message", "Invalid return request."))
    return result["return"]

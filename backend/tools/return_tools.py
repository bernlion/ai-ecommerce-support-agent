from datetime import datetime, timezone
from uuid import uuid4

from database.mongodb import get_database


def create_return_request(order_id: str, reason: str) -> dict:
    db = get_database()
    clean_id = order_id.strip().upper()
    order = db.orders.find_one({"order_id": clean_id})
    if not order:
        return {"success": False, "message": f"Order {clean_id} was not found."}
    if order["status"] != "Delivered":
        return {"success": False, "message": f"Only delivered orders can be returned. Order {clean_id} is currently {order['status']}."}
    if not reason.strip():
        return {"success": False, "message": "Please provide a reason for the return request."}

    return_doc = {
        "return_id": f"RET-{uuid4().hex[:8].upper()}",
        "order_id": clean_id,
        "customer_id": order["customer_id"],
        "reason": reason.strip(),
        "status": "Requested",
        "created_at": datetime.now(timezone.utc),
    }
    db.returns.insert_one(return_doc)
    return_doc.pop("_id", None)
    return {"success": True, "message": "Return request created successfully.", "return": return_doc}

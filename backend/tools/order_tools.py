from typing import Any

from database.mongodb import get_database
from tools.product_tools import get_product_details


def _clean_order(order: dict[str, Any]) -> dict[str, Any]:
    order.pop("_id", None)
    order["product_details"] = [
        get_product_details(product_id)
        for product_id in order.get("products", [])
    ]
    return order


def get_order_status(order_id: str) -> dict[str, Any]:
    order = get_database().orders.find_one({"order_id": order_id.strip().upper()})
    if not order:
        return {"error": f"Order {order_id} was not found."}
    return _clean_order(order)


def cancel_order(order_id: str) -> dict[str, Any]:
    db = get_database()
    clean_id = order_id.strip().upper()
    order = db.orders.find_one({"order_id": clean_id})
    if not order:
        return {"success": False, "message": f"Order {clean_id} was not found."}
    if order["status"] in {"Delivered", "Cancelled"}:
        return {"success": False, "message": f"Order {clean_id} cannot be cancelled because it is {order['status']}."}
    if order["status"] == "Out for Delivery":
        return {"success": False, "message": f"Order {clean_id} is already out for delivery and is not eligible for cancellation."}

    db.orders.update_one({"order_id": clean_id}, {"$set": {"status": "Cancelled"}})
    return {"success": True, "message": f"Order {clean_id} has been cancelled successfully.", "order": get_order_status(clean_id)}

from datetime import datetime, timezone
from typing import Any, Optional

from database.mongodb import get_database


def get_customer_memory(customer_id: str) -> dict[str, Any]:
    db = get_database()
    clean_id = customer_id.strip().upper()
    preferences = db.customer_preferences.find_one({"customer_id": clean_id}) or {
        "customer_id": clean_id,
        "preferred_brands": [],
        "categories": [],
        "budget": None,
        "previous_purchases": [],
    }
    preferences.pop("_id", None)
    recent_messages = list(
        db.conversations.find({"customer_id": clean_id}, {"_id": 0})
        .sort("created_at", -1)
        .limit(6)
    )
    return {"preferences": preferences, "recent_messages": list(reversed(recent_messages))}


def save_customer_memory(
    customer_id: str,
    preferred_brand: Optional[str] = None,
    category: Optional[str] = None,
    budget: Optional[float] = None,
    note: Optional[str] = None,
) -> dict[str, Any]:
    clean_id = customer_id.strip().upper()
    update: dict[str, Any] = {"$set": {"customer_id": clean_id, "updated_at": datetime.now(timezone.utc)}}
    add_to_set: dict[str, Any] = {}
    if preferred_brand:
        add_to_set["preferred_brands"] = preferred_brand.strip().title()
    if category:
        add_to_set["categories"] = category.strip().title()
    if note:
        update["$set"]["note"] = note.strip()
    if budget is not None:
        update["$set"]["budget"] = budget
    if add_to_set:
        update["$addToSet"] = add_to_set
    get_database().customer_preferences.update_one({"customer_id": clean_id}, update, upsert=True)
    return {"success": True, "memory": get_customer_memory(clean_id)["preferences"]}


def store_conversation(customer_id: str, user_message: str, assistant_message: str, tool_used: Optional[str]) -> str:
    doc = {
        "customer_id": customer_id.strip().upper(),
        "user_message": user_message,
        "assistant_message": assistant_message,
        "tool_used": tool_used,
        "created_at": datetime.now(timezone.utc),
    }
    result = get_database().conversations.insert_one(doc)
    return str(result.inserted_id)

from typing import Any, Optional

from database.mongodb import get_database
from tools.customer_tools import get_customer_memory


def recommend_products(customer_id: str, category: Optional[str] = None, budget: Optional[float] = None) -> dict[str, Any]:
    db = get_database()
    memory = get_customer_memory(customer_id)
    preferences = memory["preferences"]

    filters: dict[str, Any] = {"stock": {"$gt": 0}}
    chosen_category = category or (preferences.get("categories") or [None])[-1]
    chosen_budget = budget or preferences.get("budget")
    if chosen_category:
        filters["category"] = {"$regex": chosen_category, "$options": "i"}
    if chosen_budget:
        filters["price"] = {"$lte": float(chosen_budget)}

    preferred_brands = preferences.get("preferred_brands", [])
    products = []
    if preferred_brands:
        brand_filters = {**filters, "brand": {"$in": preferred_brands}}
        products.extend(list(db.products.find(brand_filters, {"_id": 0}).sort("rating", -1).limit(4)))

    if len(products) < 5:
        existing_ids = {p["product_id"] for p in products}
        for product in db.products.find(filters, {"_id": 0}).sort("rating", -1).limit(8):
            if product["product_id"] not in existing_ids:
                products.append(product)
            if len(products) >= 5:
                break

    return {
        "products": products,
        "count": len(products),
        "used_preferences": {"category": chosen_category, "budget": chosen_budget, "preferred_brands": preferred_brands},
    }

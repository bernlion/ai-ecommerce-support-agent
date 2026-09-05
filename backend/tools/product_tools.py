from typing import Any, Optional

from database.mongodb import get_database


def _clean_product(product: dict[str, Any]) -> dict[str, Any]:
    product.pop("_id", None)
    return product


def search_products(
    query: Optional[str] = None,
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    brand: Optional[str] = None,
    limit: int = 8,
) -> dict[str, Any]:
    filters: dict[str, Any] = {}
    if query:
        filters["$or"] = [
            {"name": {"$regex": query, "$options": "i"}},
            {"description": {"$regex": query, "$options": "i"}},
            {"category": {"$regex": query, "$options": "i"}},
        ]
    if category:
        filters["category"] = {"$regex": f"^{category}$", "$options": "i"}
    if brand:
        filters["brand"] = {"$regex": f"^{brand}$", "$options": "i"}
    price_filter: dict[str, float] = {}
    if min_price is not None:
        price_filter["$gte"] = min_price
    if max_price is not None:
        price_filter["$lte"] = max_price
    if price_filter:
        filters["price"] = price_filter

    products = [_clean_product(p) for p in get_database().products.find(filters).limit(max(1, min(limit, 20)))]
    return {"products": products, "count": len(products)}


def get_product_details(product_id: str) -> dict[str, Any]:
    product = get_database().products.find_one({"product_id": product_id.strip().upper()})
    if not product:
        return {"error": f"Product {product_id} was not found."}
    return _clean_product(product)

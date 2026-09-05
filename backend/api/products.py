from fastapi import APIRouter, HTTPException, Query

from tools.product_tools import get_product_details, search_products

router = APIRouter(prefix="/api/products", tags=["products"])


@router.get("")
def list_products(
    query: str | None = None,
    category: str | None = None,
    min_price: float | None = Query(default=None, ge=0),
    max_price: float | None = Query(default=None, ge=0),
    brand: str | None = None,
):
    return search_products(query=query, category=category, min_price=min_price, max_price=max_price, brand=brand, limit=20)


@router.get("/{product_id}")
def product_details(product_id: str):
    result = get_product_details(product_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

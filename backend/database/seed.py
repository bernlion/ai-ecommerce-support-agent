from datetime import datetime, timedelta, timezone

from database.mongodb import ensure_indexes, get_database


PRODUCTS = [
    {"product_id": "P1001", "name": "Samsung Galaxy S24", "description": "Flagship Android phone with AMOLED display and AI camera tools.", "price": 58999, "brand": "Samsung", "category": "Smartphones", "stock": 18, "rating": 4.6},
    {"product_id": "P1002", "name": "Apple iPhone 15", "description": "A16-powered iPhone with Dynamic Island and excellent camera quality.", "price": 69900, "brand": "Apple", "category": "Smartphones", "stock": 9, "rating": 4.7},
    {"product_id": "P1003", "name": "OnePlus Nord CE 4", "description": "Fast mid-range smartphone with long battery life.", "price": 24999, "brand": "OnePlus", "category": "Smartphones", "stock": 32, "rating": 4.3},
    {"product_id": "P1004", "name": "Lenovo IdeaPad Slim 5", "description": "Everyday laptop with Ryzen 7, 16GB RAM, and 512GB SSD.", "price": 57990, "brand": "Lenovo", "category": "Laptops", "stock": 13, "rating": 4.4},
    {"product_id": "P1005", "name": "ASUS TUF Gaming F15", "description": "Gaming laptop with Intel i5, RTX graphics, and 144Hz display.", "price": 71990, "brand": "ASUS", "category": "Laptops", "stock": 7, "rating": 4.5},
    {"product_id": "P1006", "name": "HP 15s Student Laptop", "description": "Lightweight laptop for students with Intel i5 and full HD display.", "price": 52999, "brand": "HP", "category": "Laptops", "stock": 16, "rating": 4.2},
    {"product_id": "P1007", "name": "Sony WH-CH720N", "description": "Wireless noise-cancelling headphones with up to 35 hours battery.", "price": 8990, "brand": "Sony", "category": "Headphones", "stock": 25, "rating": 4.4},
    {"product_id": "P1008", "name": "boAt Rockerz 450", "description": "Affordable wireless headphones with punchy bass.", "price": 1499, "brand": "boAt", "category": "Headphones", "stock": 60, "rating": 4.0},
    {"product_id": "P1009", "name": "Samsung Galaxy Watch6", "description": "Smart watch with health tracking and Wear OS apps.", "price": 22999, "brand": "Samsung", "category": "Smart Watches", "stock": 11, "rating": 4.5},
    {"product_id": "P1010", "name": "Apple iPad 10th Gen", "description": "10.9-inch tablet for study, entertainment, and creative work.", "price": 34900, "brand": "Apple", "category": "Tablets", "stock": 14, "rating": 4.6},
    {"product_id": "P1011", "name": "Samsung Galaxy Tab S9 FE", "description": "Android tablet with S Pen support and vivid display.", "price": 32999, "brand": "Samsung", "category": "Tablets", "stock": 10, "rating": 4.4},
    {"product_id": "P1012", "name": "Logitech Pebble Mouse 2", "description": "Compact Bluetooth mouse for laptops and tablets.", "price": 2295, "brand": "Logitech", "category": "Accessories", "stock": 45, "rating": 4.3},
]

CUSTOMERS = [
    {"customer_id": "C1001", "name": "Aarav Sharma", "email": "aarav@example.com"},
    {"customer_id": "C1002", "name": "Diya Rao", "email": "diya@example.com"},
    {"customer_id": "C1003", "name": "Kabir Mehta", "email": "kabir@example.com"},
    {"customer_id": "C1004", "name": "Nisha Iyer", "email": "nisha@example.com"},
    {"customer_id": "C1005", "name": "Rohan Gupta", "email": "rohan@example.com"},
]


def _order(order_id: str, customer_id: str, products: list[str], status: str, days_ago: int, delivery_in: int):
    return {
        "order_id": order_id,
        "customer_id": customer_id,
        "products": products,
        "status": status,
        "order_date": (datetime.now(timezone.utc) - timedelta(days=days_ago)).isoformat(),
        "expected_delivery": (datetime.now(timezone.utc) + timedelta(days=delivery_in)).date().isoformat(),
    }


ORDERS = [
    _order("ORD1001", "C1001", ["P1004"], "Shipped", 2, 3),
    _order("ORD1002", "C1001", ["P1007", "P1012"], "Processing", 1, 5),
    _order("ORD1003", "C1001", ["P1009"], "Delivered", 12, -4),
    _order("ORD1004", "C1002", ["P1001"], "Out for Delivery", 3, 0),
    _order("ORD1005", "C1002", ["P1010"], "Delivered", 20, -12),
    _order("ORD1006", "C1003", ["P1005"], "Processing", 0, 6),
    _order("ORD1007", "C1003", ["P1008"], "Cancelled", 5, 0),
    _order("ORD1008", "C1004", ["P1003"], "Shipped", 4, 2),
    _order("ORD1009", "C1005", ["P1011"], "Delivered", 16, -8),
    _order("ORD1010", "C1005", ["P1006"], "Processing", 1, 4),
]


def seed_database() -> None:
    db = get_database()
    ensure_indexes()
    if db.products.count_documents({}) == 0:
        db.products.insert_many(PRODUCTS)
    if db.customers.count_documents({}) == 0:
        db.customers.insert_many(CUSTOMERS)
    if db.orders.count_documents({}) == 0:
        db.orders.insert_many(ORDERS)
    for customer in CUSTOMERS:
        db.customer_preferences.update_one(
            {"customer_id": customer["customer_id"]},
            {"$setOnInsert": {"customer_id": customer["customer_id"], "preferred_brands": [], "categories": [], "budget": None, "previous_purchases": []}},
            upsert=True,
        )


if __name__ == "__main__":
    seed_database()
    print("Seed data loaded.")

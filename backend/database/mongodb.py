import os
from functools import lru_cache

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.database import Database

load_dotenv()


@lru_cache
def get_client() -> MongoClient:
    uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    return MongoClient(uri, serverSelectionTimeoutMS=2500)


def get_database() -> Database:
    name = os.getenv("DATABASE_NAME", "ecommerce_agent")
    return get_client()[name]


def check_connection() -> bool:
    try:
        get_client().admin.command("ping")
        return True
    except Exception:
        return False


def ensure_indexes() -> None:
    db = get_database()
    db.products.create_index([("name", "text"), ("category", "text"), ("brand", "text")])
    db.products.create_index("product_id", unique=True)
    db.customers.create_index("customer_id", unique=True)
    db.orders.create_index("order_id", unique=True)
    db.returns.create_index("return_id", unique=True)
    db.conversations.create_index([("customer_id", 1), ("created_at", -1)])
    db.customer_preferences.create_index("customer_id", unique=True)

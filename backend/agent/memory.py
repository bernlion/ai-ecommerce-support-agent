import re
from typing import Optional

from tools.customer_tools import save_customer_memory


BRANDS = ["Samsung", "Apple", "OnePlus", "Lenovo", "ASUS", "HP", "Sony", "boAt", "Logitech"]
CATEGORIES = ["Smartphones", "Laptops", "Headphones", "Smart Watches", "Tablets", "Accessories"]


def infer_and_save_preferences(customer_id: str, message: str) -> Optional[dict]:
    lower = message.lower()
    if not any(word in lower for word in ["prefer", "like", "budget", "recommend", "interested"]):
        return None

    brand = next((b for b in BRANDS if b.lower() in lower), None)
    category = next((c for c in CATEGORIES if c.lower() in lower or c.lower().rstrip("s") in lower), None)
    budget_match = re.search(r"(?:under|below|budget|less than|upto|up to)\s*(?:rs\.?|₹|inr)?\s*(\d{3,7})", lower)
    budget = float(budget_match.group(1)) if budget_match else None
    if not any([brand, category, budget]):
        return None
    return save_customer_memory(customer_id, preferred_brand=brand, category=category, budget=budget, note=message)

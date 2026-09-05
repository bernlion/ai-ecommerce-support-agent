import json
import re
from typing import Any, Callable

from agent.memory import infer_and_save_preferences
from agent.ollama_client import OllamaClient
from agent.prompts import SYSTEM_PROMPT, TOOL_SELECTION_PROMPT
from tools.customer_tools import get_customer_memory, save_customer_memory, store_conversation
from tools.order_tools import cancel_order, get_order_status
from tools.product_tools import get_product_details, search_products
from tools.recommendation_tools import recommend_products
from tools.return_tools import create_return_request

ToolFn = Callable[..., dict[str, Any]]


class EcommerceSupportAgent:
    def __init__(self) -> None:
        self.llm = OllamaClient()
        self.tools: dict[str, ToolFn] = {
            "search_products": search_products,
            "get_product_details": get_product_details,
            "get_order_status": get_order_status,
            "cancel_order": cancel_order,
            "create_return_request": create_return_request,
            "recommend_products": recommend_products,
            "get_customer_memory": get_customer_memory,
            "save_customer_memory": save_customer_memory,
        }

    async def handle_message(self, customer_id: str, message: str) -> dict[str, Any]:
        clean_customer_id = customer_id.strip().upper()
        clean_message = message.strip()
        if not clean_message:
            raise ValueError("Message cannot be empty.")

        memory = get_customer_memory(clean_customer_id)
        inferred_memory = infer_and_save_preferences(clean_customer_id, clean_message)
        if inferred_memory:
            memory = get_customer_memory(clean_customer_id)

        selection = await self._select_tool(clean_customer_id, clean_message, memory)
        tool_name = selection.get("tool", "none")
        args = selection.get("arguments", {}) if isinstance(selection.get("arguments"), dict) else {}
        tool_result: dict[str, Any] | None = None
        products: list[dict[str, Any]] = []

        if tool_name in self.tools and tool_name != "none":
            args = self._sanitize_args(tool_name, clean_customer_id, args)
            tool_result = self.tools[tool_name](**args)
            products = self._extract_products(tool_result)
            if tool_name == "save_customer_memory":
                memory = get_customer_memory(clean_customer_id)
        elif inferred_memory and self._is_preference_message(clean_message):
            tool_name = "save_customer_memory"
            tool_result = inferred_memory

        response = await self._final_response(clean_message, memory, tool_name, tool_result)
        conversation_id = store_conversation(clean_customer_id, clean_message, response, None if tool_name == "none" else tool_name)
        return {
            "response": response,
            "tool_used": None if tool_name == "none" else tool_name,
            "conversation_id": conversation_id,
            "products": products,
        }

    async def _select_tool(self, customer_id: str, message: str, memory: dict[str, Any]) -> dict[str, Any]:
        if self._is_greeting(message):
            return {"tool": "none", "arguments": {}}

        heuristic = self._heuristic_tool(customer_id, message)
        if heuristic:
            return heuristic

        prompt = f"{TOOL_SELECTION_PROMPT}\nCustomer ID: {customer_id}\nMemory: {json.dumps(memory, default=str)}\nMessage: {message}"
        try:
            raw = await self.llm.generate(prompt, system=SYSTEM_PROMPT, format_json=True)
            parsed = json.loads(raw)
            if parsed.get("tool") in {*self.tools.keys(), "none"}:
                return parsed
        except Exception:
            pass
        return {"tool": "none", "arguments": {}}

    async def _final_response(self, message: str, memory: dict[str, Any], tool_name: str, tool_result: dict[str, Any] | None) -> str:
        if tool_name != "none" and tool_result is not None:
            return self._fallback_response(tool_name, tool_result)
        if self._is_greeting(message):
            return "Hello! I can help you find products, check order status, cancel eligible orders, create return requests, or recommend items."

        prompt = (
            f"Customer message: {message}\n"
            f"Customer memory: {json.dumps(memory, default=str)}\n"
            f"Tool used: {tool_name}\n"
            f"Tool result: {json.dumps(tool_result, default=str)}\n"
            "Write the final customer support response."
        )
        try:
            return await self.llm.generate(prompt, system=SYSTEM_PROMPT)
        except RuntimeError as exc:
            if tool_result:
                return self._fallback_response(tool_name, tool_result)
            return str(exc)

    def _heuristic_tool(self, customer_id: str, message: str) -> dict[str, Any] | None:
        lower = message.lower()
        order_id = self._match_id(message, r"ORD\d+")
        product_id = self._match_id(message, r"P\d+")
        budget = self._match_budget(lower)
        category = self._match_category(lower)
        brand = self._match_brand(lower)

        if self._is_preference_message(message):
            return {"tool": "save_customer_memory", "arguments": {"customer_id": customer_id, "preferred_brand": brand, "category": category, "budget": budget, "note": message}}
        if "return" in lower and order_id:
            reason = re.sub(r".*because", "", message, flags=re.IGNORECASE).strip() if "because" in lower else message
            return {"tool": "create_return_request", "arguments": {"order_id": order_id, "reason": reason}}
        if any(word in lower for word in ["cancel", "cancellation"]) and order_id:
            return {"tool": "cancel_order", "arguments": {"order_id": order_id}}
        if order_id and any(word in lower for word in ["where", "status", "order", "delivery", "track"]):
            return {"tool": "get_order_status", "arguments": {"order_id": order_id}}
        if product_id:
            return {"tool": "get_product_details", "arguments": {"product_id": product_id}}
        if any(word in lower for word in ["recommend", "suggest", "best for me"]):
            return {"tool": "recommend_products", "arguments": {"customer_id": customer_id, "category": category, "budget": budget}}
        if any(word in lower for word in ["find", "search", "show", "products", "laptop", "phone", "headphone", "tablet", "watch"]):
            return {"tool": "search_products", "arguments": {"query": category or brand or message, "category": category, "max_price": budget, "brand": brand}}
        if self._looks_like_product_query(lower):
            return {"tool": "search_products", "arguments": {"query": message, "max_price": budget, "brand": brand}}
        return None

    def _sanitize_args(self, tool_name: str, customer_id: str, args: dict[str, Any]) -> dict[str, Any]:
        allowed = {
            "search_products": {"query", "category", "min_price", "max_price", "brand", "limit"},
            "get_product_details": {"product_id"},
            "get_order_status": {"order_id"},
            "cancel_order": {"order_id"},
            "create_return_request": {"order_id", "reason"},
            "recommend_products": {"customer_id", "category", "budget"},
            "get_customer_memory": {"customer_id"},
            "save_customer_memory": {"customer_id", "preferred_brand", "category", "budget", "note"},
        }
        safe = {key: value for key, value in args.items() if key in allowed.get(tool_name, set()) and value not in ["", None]}
        if "customer_id" in allowed.get(tool_name, set()):
            safe["customer_id"] = customer_id
        return safe

    def _fallback_response(self, tool_name: str, result: dict[str, Any]) -> str:
        if "error" in result:
            return result["error"]
        if result.get("message"):
            return result["message"]
        if tool_name in {"search_products", "recommend_products"}:
            products = result.get("products", [])
            if not products:
                return "I checked the catalog, but I could not find matching available products right now. Try another product name, brand, category, or budget."
            names = ", ".join(f"{p['name']} at ₹{p['price']}" for p in products[:4])
            return f"Here are some options I found: {names}."
        if tool_name == "get_order_status":
            return f"Order {result['order_id']} is {result['status']}. Expected delivery: {result['expected_delivery']}."
        if tool_name == "save_customer_memory":
            memory = result.get("memory", {})
            brands = ", ".join(memory.get("preferred_brands", [])) or "your preferred brands"
            categories = ", ".join(memory.get("categories", [])) or "your preferred categories"
            return f"Got it. I saved your preference for {brands} and {categories}."
        return "I have handled that request."

    def _extract_products(self, result: dict[str, Any] | None) -> list[dict[str, Any]]:
        if not isinstance(result, dict):
            return []
        products = result.get("products", [])
        if isinstance(products, list) and all(isinstance(item, dict) for item in products):
            return products
        return []

    def _is_preference_message(self, message: str) -> bool:
        return any(word in message.lower() for word in ["prefer", "like", "budget"])

    def _is_greeting(self, message: str) -> bool:
        return message.strip().lower() in {"hello", "hi", "hey", "good morning", "good afternoon", "good evening"}

    def _looks_like_product_query(self, lower: str) -> bool:
        support_words = [
            "hello",
            "hi",
            "hey",
            "thanks",
            "thank you",
            "order",
            "cancel",
            "return",
            "refund",
            "delivery",
            "status",
            "track",
        ]
        if any(word in lower for word in support_words):
            return False
        words = re.findall(r"[a-z0-9]+", lower)
        return 1 <= len(words) <= 5

    def _match_id(self, message: str, pattern: str) -> str | None:
        match = re.search(pattern, message, flags=re.IGNORECASE)
        return match.group(0).upper() if match else None

    def _match_budget(self, lower: str) -> float | None:
        match = re.search(r"(?:under|below|budget|less than|upto|up to)\s*(?:rs\.?|₹|inr)?\s*(\d{3,7})", lower)
        return float(match.group(1)) if match else None

    def _match_category(self, lower: str) -> str | None:
        mapping = {
            "phone": "Smartphones",
            "smartphone": "Smartphones",
            "laptop": "Laptops",
            "headphone": "Headphones",
            "watch": "Smart Watches",
            "tablet": "Tablets",
            "accessor": "Accessories",
        }
        return next((category for key, category in mapping.items() if key in lower), None)

    def _match_brand(self, lower: str) -> str | None:
        brands = ["Samsung", "Apple", "OnePlus", "Lenovo", "ASUS", "HP", "Sony", "boAt", "Logitech"]
        return next((brand for brand in brands if brand.lower() in lower), None)

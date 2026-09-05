import os
from typing import Any

import httpx
from dotenv import load_dotenv

load_dotenv()


class OllamaClient:
    def __init__(self) -> None:
        self.host = os.getenv("OLLAMA_HOST", "http://localhost:11434").rstrip("/")
        self.model = os.getenv("OLLAMA_MODEL", "gemma3:4b")

    async def generate(self, prompt: str, system: str | None = None, format_json: bool = False) -> str:
        payload: dict[str, Any] = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.2},
        }
        if system:
            payload["system"] = system
        if format_json:
            payload["format"] = "json"

        try:
            async with httpx.AsyncClient(timeout=60) as client:
                response = await client.post(f"{self.host}/api/generate", json=payload)
                response.raise_for_status()
                return response.json().get("response", "").strip()
        except httpx.ConnectError as exc:
            raise RuntimeError("Ollama is not running. Start Ollama and run: ollama pull gemma3:4b") from exc
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 404:
                raise RuntimeError("Gemma model is missing. Run: ollama pull gemma3:4b") from exc
            raise RuntimeError(f"Ollama returned an error: {exc.response.text}") from exc

    async def health(self) -> dict[str, Any]:
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                tags = await client.get(f"{self.host}/api/tags")
                tags.raise_for_status()
                models = [m.get("name") for m in tags.json().get("models", [])]
                return {"running": True, "model": self.model, "model_available": self.model in models}
        except Exception:
            return {"running": False, "model": self.model, "model_available": False}

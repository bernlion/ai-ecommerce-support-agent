from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from agent.ollama_client import OllamaClient
from api.chat import router as chat_router
from api.orders import router as orders_router
from api.products import router as products_router
from database.mongodb import check_connection
from database.seed import seed_database

app = FastAPI(title="AI E-Commerce Customer Support Agent", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)
app.include_router(products_router)
app.include_router(orders_router)


@app.on_event("startup")
def startup() -> None:
    if check_connection():
        seed_database()


@app.get("/api/health")
async def health():
    mongo_ok = check_connection()
    ollama = await OllamaClient().health()
    return {
        "status": "ok" if mongo_ok and ollama["running"] else "degraded",
        "mongodb": mongo_ok,
        "ollama": ollama,
    }

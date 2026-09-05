# AI E-Commerce Customer Support Agent

A complete local AI customer-support demo for an e-commerce store. The React chat UI talks to a FastAPI backend, the backend calls a Python support agent, the agent uses Ollama with `gemma3:4b`, and factual store actions are handled through MongoDB-backed tools.

## Architecture

User -> React Chat Interface -> FastAPI Backend -> Python AI Agent -> Ollama/Gemma -> Tool Selection -> MongoDB Tools -> Final Response.

The agent uses a dependable Python tool layer for product search, product details, order status, cancellation, return requests, recommendations, short-term conversation memory, and long-term customer preference memory.

## Technology Stack

- Frontend: React, Vite, JavaScript, HTML, CSS
- Backend: Python, FastAPI, Uvicorn
- AI: Ollama with `gemma3:4b`
- Database: MongoDB with PyMongo

## Folder Structure

```text
backend/
  agent/        Ollama client, prompts, memory extraction, support agent
  api/          FastAPI route modules
  database/     MongoDB connection, Pydantic models, seed data
  tools/        Product, order, return, customer, and recommendation tools
frontend/
  src/          React app, API client, components, styles
data/           Human-readable sample products, customers, and orders
```

## Installation

Install Python 3.10+, Node.js 18+, MongoDB Community Server, and Ollama.

## Ollama and Gemma

```bat
ollama pull gemma3:4b
ollama run gemma3:4b
```

The backend reads Ollama settings from environment variables:

```text
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=gemma3:4b
MONGODB_URI=mongodb://localhost:27017
DATABASE_NAME=ecommerce_agent
```

Copy `backend\.env.example` to `backend\.env` if you need to change defaults.

## MongoDB Setup

Start MongoDB locally. The FastAPI app seeds the database on startup when MongoDB is reachable. You can also seed manually:

```bat
cd C:\IBM-intern\PROJECT\backend
python database\seed.py
```

Collections created: `products`, `customers`, `orders`, `returns`, `conversations`, and `customer_preferences`.

## Backend Setup

```bat
cd C:\IBM-intern\PROJECT\backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

## Frontend Setup

```bat
cd C:\IBM-intern\PROJECT\frontend
npm install
npm run dev
```

Open `http://localhost:5173`.

## One-Click Windows Runner

```bat
cd C:\IBM-intern\PROJECT
run_project.bat
```

This opens separate backend and frontend command windows. MongoDB and Ollama should already be running.

## API Endpoints

- `GET /api/health`
- `POST /api/chat`
- `GET /api/products`
- `GET /api/products/{product_id}`
- `GET /api/orders/{order_id}`
- `POST /api/returns`

Example chat request:

```json
{
  "customer_id": "C1001",
  "message": "Where is my order ORD1001?"
}
```

## Tool Calling

The agent first uses deterministic Python heuristics for common support cases such as order IDs, product IDs, cancellation, returns, search, recommendations, and preference statements. For other messages, it asks Gemma to return strict JSON containing a tool name and arguments. The backend validates the tool name and argument keys before executing anything. It never runs arbitrary model-generated code.

Available tools: `search_products`, `get_product_details`, `get_order_status`, `cancel_order`, `create_return_request`, `recommend_products`, `get_customer_memory`, and `save_customer_memory`.

## Memory

Short-term memory is stored in the `conversations` collection as recent customer turns. Long-term memory is stored in `customer_preferences`, including preferred brands, categories, budget, notes, and previous-purchase-ready fields. Recommendation tools retrieve this memory before selecting products.

## Testing Instructions

After MongoDB, Ollama, backend, and frontend are running, try:

- `Find laptops under ₹60000`
- `Where is my order ORD1001?`
- `I want to cancel ORD1002`
- `I want to return ORD1003 because it is damaged`
- `I prefer Samsung phones`
- `Recommend a phone for me`
- `Hello`

Expected tool use:

- Product search for laptop search
- Order status for `ORD1001`
- Cancellation eligibility check for `ORD1002`
- Return request creation for delivered `ORD1003`
- Preference memory save for Samsung phones
- Recommendation with Samsung preference for phone recommendation
- No unnecessary tool call for `Hello`

## Troubleshooting

- Ollama offline: start Ollama and run `ollama pull gemma3:4b`.
- Gemma missing: run `ollama pull gemma3:4b`.
- MongoDB unavailable: start the MongoDB service and confirm `mongodb://localhost:27017`.
- Frontend cannot reach backend: confirm FastAPI is running at `http://localhost:8000`.
- Empty message: the API returns a validation error.
- Invalid order or product ID: the API returns a friendly 404 or support response.

## Future Improvements

- Add login and authenticated customer sessions.
- Add admin dashboards for returns and support analytics.
- Add vector search over product descriptions.
- Add unit tests with mocked MongoDB and Ollama.
- Add streaming responses from Ollama.

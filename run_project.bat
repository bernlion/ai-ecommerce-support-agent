@echo off
setlocal
echo Starting AI E-Commerce Customer Support Agent...
echo.
echo Make sure MongoDB is running and Ollama has gemma3:4b installed.
echo.
start "FastAPI Backend" cmd /k "cd /d C:\IBM-intern\PROJECT\backend && if not exist venv python -m venv venv && call venv\Scripts\activate && pip install -r requirements.txt && uvicorn main:app --reload --port 8000"
start "React Frontend" cmd /k "cd /d C:\IBM-intern\PROJECT\frontend && npm install && npm run dev"
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173
endlocal

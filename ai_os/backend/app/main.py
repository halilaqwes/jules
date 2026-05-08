from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import socketio
import uvicorn
import asyncio
from .services.ollama_service import ollama_service
from .services.memory_service import memory_service
from .agents.orchestrator import orchestrator

app = FastAPI(title="AI OS Backend")

@app.on_event("shutdown")
def shutdown_event():
    orchestrator.stop()

# Setup CORS - Allow Vite dev server and Electron app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "file://", "app://."],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup Socket.IO - Allow specific origins and Electron protocol
sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins="*" # We must allow * for electron apps loading via file:// or custom protocols, but the API itself runs entirely locally.
)
sio_app = socketio.ASGIApp(sio, other_asgi_app=app)

@app.on_event("startup")
async def startup_event():
    import os
    # Ensure skills are downloaded on startup if missing
    skills_dir = os.path.join(os.path.dirname(__file__), "skills", "data")
    if not os.path.exists(skills_dir) or len(os.listdir(skills_dir)) < 100:
        import subprocess
        import sys
        print("Running skill downloader...")
        subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), "..", "download_skills.py")])

    # Start the 24/7 background agent loop
    import asyncio
    asyncio.create_task(orchestrator.run_loop())

@app.get("/api/models")
async def get_models():
    models = await ollama_service.list_models()
    return {"models": models}

@app.post("/api/memory")
async def save_memory(data: dict):
    key = data.get("key")
    value = data.get("value")
    if key and value:
        memory_service.set_memory(key, value)
        return {"status": "success"}
    return {"status": "error", "message": "Key and value required"}

@app.get("/api/tools")
async def get_tools():
    """Endpoint for extensions/plugins to list loaded tools."""
    from .tools.tool_manager import tool_manager
    tools = [{"name": name, "description": t["description"]} for name, t in tool_manager.tools.items()]
    return {"tools": tools}

@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")

@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")

@sio.event
async def set_goal(sid, data: dict):
    goal = data.get("goal")
    model = data.get("model")
    print(f"Setting goal for orchestrator: {goal} with model {model}")
    if model:
        orchestrator.set_model(model)
    if goal:
        orchestrator.set_goal(goal)
    await sio.emit("agent_status", {"status": "goal_set", "goal": goal}, room=sid)

@sio.event
async def chat_message(sid, data: dict):
    """Handle incoming chat message from the user."""
    message = data.get("message")
    model = data.get("model")
    if model:
        orchestrator.set_model(model)

    if message:
        print(f"Received chat message: {message}")
        # Send an immediate processing status
        await sio.emit("chat_status", {"status": "thinking"}, room=sid)

        # Get AI response
        response = await orchestrator.handle_chat_message(message)

        # Reply back
        await sio.emit("chat_reply", {"message": response}, room=sid)

# Forwarding memory logs to socketio clients for real-time dashboard tracking
def log_event_hook(agent_id, event_type, content):
    asyncio.create_task(sio.emit("agent_log", {"agent": agent_id, "type": event_type, "content": content}))

memory_service.log_event_hook = log_event_hook

if __name__ == "__main__":
    uvicorn.run("app.main:sio_app", host="127.0.0.1", port=8000, reload=True)

"""AgentHive SaaS — Production FastAPI Application."""
import os
import json as _json
import asyncio
from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI, Request, Depends, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from sqlmodel import select

from . import agents, auth, billing, models
from .models import Task, User, get_session, engine, init_db, UserRole
from .agents import model_router
from .websocket import manager


# ============================================================================
# Environment & Configuration
# ============================================================================
def load_env():
    """Load .env file if it exists."""
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, _, value = line.partition("=")
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                if key and key not in os.environ:
                    os.environ[key] = value
        print(f"[OK] Loaded .env from {env_path}")
    else:
        print(f"[WARN] No .env file found — using system env vars only")


# ============================================================================
# WebSocket Manager for Real-Time Updates
# ============================================================================
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                pass


manager = ConnectionManager()


# ============================================================================
# App Lifespan
# ============================================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    load_env()
    init_db()
    await model_router.reload_configs()
    yield


# ============================================================================
# App Creation
# ============================================================================
app = FastAPI(
    title="AgentHive — Multi-Agent SaaS Platform",
    version="1.0.0",
    description="AI Agent Workspace with 5 specialist agents, real-time dashboard, and subscription billing",
    lifespan=lifespan,
)

# Security Middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"],
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_static_dir = os.path.join(_project_root, "static").replace("\\", "/")
_templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates").replace("\\", "/")

app.mount("/static", StaticFiles(directory=_static_dir), name="static")
templates = Jinja2Templates(directory=_templates_dir)


def render_template(name: str, context: dict = None) -> HTMLResponse:
    """Read HTML file and inject basic context variables."""
    path = os.path.join(_templates_dir, name)
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    if context:
        for k, v in context.items():
            html = html.replace(f"{{{{ {k} }}}}", str(v))
    return HTMLResponse(content=html)


# ============================================================================
# Include Routers
# ============================================================================
app.include_router(auth.router)
app.include_router(billing.router)

# ============================================================================
# Public Pages
# ============================================================================

@app.get("/", response_class=HTMLResponse)
async def landing(request: Request):
    return render_template("landing.html", {"title": "AgentHive"})


@app.get("/pricing", response_class=HTMLResponse)
async def pricing(request: Request):
    return render_template("pricing.html", {"title": "Pricing — AgentHive"})


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return render_template("login.html", {"title": "Login — AgentHive"})


@app.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    return render_template("signup.html", {"title": "Signup — AgentHive"})


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, user: User = Depends(auth.get_current_active_user)):
    with get_session() as session:
        total = len(session.exec(select(Task)).where(Task.user_id == user.id).all())
        active = len(session.exec(select(Task).where(
            Task.user_id == user.id, Task.status == "running"
        )).all())
        completed = len(session.exec(select(Task).where(
            Task.user_id == user.id, Task.status == "completed"
        )).all())
    
    stats = {"total_tasks": total, "active": active, "completed": completed}
    
    html_path = os.path.join(_templates_dir, "dashboard.html")
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    
    html = html.replace("{{ stats.total_tasks }}", str(total))
    html = html.replace("{{ stats.active }}", str(active))
    html = html.replace("{{ stats.completed }}", str(completed))
    html = html.replace("{{ user.email.split('@')[0] }}", user.email.split('@')[0])
    html = html.replace("{{ user.email }}", user.email)
    
    return HTMLResponse(content=html)


# ============================================================================
# API Endpoints
# ============================================================================

@app.get("/api/tasks/stats")
async def task_stats(user: User = Depends(auth.get_current_active_user)):
    with get_session() as session:
        total = len(session.exec(select(Task).where(Task.user_id == user.id)).all())
        active = len(session.exec(select(Task).where(
            Task.user_id == user.id, Task.status == "running"
        )).all())
        completed = len(session.exec(select(Task).where(
            Task.user_id == user.id, Task.status == "completed"
        )).all())
        return {"total": total, "active": active, "completed": completed}


@app.get("/api/tasks/recent")
async def recent_tasks(user: User = Depends(auth.get_current_active_user)):
    with get_session() as session:
        statement = select(Task).where(Task.user_id == user.id).order_by(
            Task.created_at.desc()
        ).limit(10)
        tasks = session.exec(statement).all()
        return [
            {
                "id": t.id,
                "title": t.title,
                "status": t.status,
                "agent_type": t.agent_type,
                "created_at": t.created_at.isoformat() if t.created_at else "",
            }
            for t in tasks
        ]


@app.get("/api/agents/status")
async def agent_status():
    return {
        "agents": [
            {"name": "Head Agent (Orchestrator)", "type": "orchestrator", "status": "active"},
            {"name": "Trend Scout", "type": "research", "status": "active"},
            {"name": "Analyst", "type": "analytics", "status": "active"},
            {"name": "Creative Studio", "type": "content", "status": "active"},
            {"name": "Social Media Manager", "type": "social", "status": "active"},
        ],
        "models": [
            {"name": "deepseek-chat", "provider": "deepseek", "active": model_router.current_idx == 0},
            {"name": "groq/llama-3.1-70b", "provider": "groq", "active": model_router.current_idx == 1},
            {"name": "gpt-4o-mini", "provider": "openai", "active": model_router.current_idx == 2},
        ]
    }


@app.post("/api/tasks")
async def create_task(
    payload: models.TaskCreate,
    user: User = Depends(auth.get_current_active_user),
):
    """Create a new task and trigger the agent pipeline."""
    # Check plan limits
    from .auth import check_plan_limits
    plan = check_plan_limits(user, get_session(), required_agent="head_agent")
    
    with get_session() as session:
        task = Task(
            user_id=user.id,
            title=payload.title,
            description=payload.description,
            status="running",
        )
        session.add(task)
        session.commit()
        task_id = task.id

    task_status = "running"
    task_result = None

    try:
        task_result = await agents.orchestrate(task_id)
        task_result = _json.dumps(task_result)
        task_status = "completed"
        with get_session() as session:
            task = session.get(Task, task_id)
            task.status = task_status
            task.result = task_result
            task.agent_type = "multi_agent"
            session.commit()
            
            # Broadcast real-time update
            await manager.broadcast({
                "type": "task_completed",
                "task_id": task_id,
                "status": "completed",
            })
    except Exception as e:
        task_status = "failed"
        task_result = str(e)
        with get_session() as session:
            task = session.get(Task, task_id)
            task.status = task_status
            task.error = task_result
            session.commit()
            
            await manager.broadcast({
                "type": "task_failed",
                "task_id": task_id,
                "status": "failed",
                "error": str(e),
            })

    return {"task_id": task_id, "status": task_status, "result": task_result}


@app.get("/health")
async def health():
    return {"status": "ok", "version": "1.0.0"}


# ============================================================================
# WebSocket for Real-Time Updates
# ============================================================================

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)


# ============================================================================
# Run
# ============================================================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8000")), reload=False)

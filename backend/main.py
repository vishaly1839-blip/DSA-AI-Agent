"""
DSA AI Tutor Agent - FastAPI Backend
REST API for the DSA AI Tutor Agent
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional, List, Dict
import uvicorn
import os

# Initialize FastAPI app
app = FastAPI(
    title="DSA AI Tutor API",
    description="AI-powered DSA learning assistant API",
    version="1.0.0"
)

security = HTTPBearer()

# In-memory storage (replace with PostgreSQL in production)
users_db: Dict = {}
sessions_db: Dict = {}
progress_db: Dict = {}


# Request/Response Models
class UserCreate(BaseModel):
    user_id: str
    username: str
    email: Optional[str] = ""


class UserLogin(BaseModel):
    user_id: str


class MessageRequest(BaseModel):
    user_id: str
    message: str


class QuizRequest(BaseModel):
    user_id: str
    topic: str = "random"
    count: int = 5


class CodeRequest(BaseModel):
    user_id: str
    code: str
    input_data: Optional[str] = ""


class ProgressUpdate(BaseModel):
    user_id: str
    topic: str
    correct: bool
    time_spent: float = 0.0


# Auth (simplified - use JWT in production)
async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """Verify authentication token"""
    # In production, verify JWT token here
    return credentials.credentials


# Health check
@app.get("/")
async def root():
    return {"message": "DSA AI Tutor API", "status": "running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


# User endpoints
@app.post("/api/users/register")
async def register_user(user: UserCreate):
    """Register a new user"""
    if user.user_id in users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    
    users_db[user.user_id] = {
        "user_id": user.user_id,
        "username": user.username,
        "email": user.email,
        "level": "Beginner",
        "created_at": "2024-01-01"
    }
    
    progress_db[user.user_id] = {
        "topics_covered": [],
        "problems_attempted": 0,
        "weak_topics": []
    }
    
    return {"status": "success", "user_id": user.user_id}


@app.post("/api/users/login")
async def login_user(user: UserLogin):
    """Login user"""
    if user.user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    # In production, return JWT token here
    return {
        "status": "success",
        "token": f"token_{user.user_id}",
        "user": users_db[user.user_id]
    }


@app.get("/api/users/{user_id}")
async def get_user(user_id: str):
    """Get user profile"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    return users_db[user_id]


# Chat endpoints
@app.post("/api/chat")
async def chat(request: MessageRequest):
    """Process chat message"""
    if request.user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Import and use agent
    from agent.core import DSAAgent
    
    agent = DSAAgent()
    response = agent.chat(request.message)
    
    return {
        "user_id": request.user_id,
        "message": request.message,
        "response": response
    }


# Quiz endpoints
@app.post("/api/quiz/start")
async def start_quiz(request: QuizRequest):
    """Start a quiz"""
    if request.user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    from agent.quiz import QuizManager
    
    manager = QuizManager()
    response = manager.start(request.topic, request.count)
    
    return {
        "user_id": request.user_id,
        "topic": request.topic,
        "message": response
    }


# Code execution endpoints
@app.post("/api/code/execute")
async def execute_code(request: CodeRequest):
    """Execute Python code"""
    if request.user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    from agent.executor import CodeExecutor
    
    executor = CodeExecutor()
    result = executor.execute(request.code, request.input_data)
    
    return {
        "success": result.success,
        "output": result.output,
        "error": result.error,
        "execution_time": result.execution_time
    }


# Progress endpoints
@app.post("/api/progress/update")
async def update_progress(update: ProgressUpdate):
    """Update user progress"""
    if update.user_id not in progress_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    progress = progress_db[update.user_id]
    
    if update.topic not in progress["topics_covered"]:
        progress["topics_covered"].append(update.topic)
    
    progress["problems_attempted"] += 1
    
    # Update weak topics if incorrect
    if not update.correct:
        if "weak_topics" not in progress:
            progress["weak_topics"] = []
        if update.topic not in progress["weak_topics"]:
            progress["weak_topics"].append(update.topic)
    
    return {"status": "success", "progress": progress}


@app.get("/api/progress/{user_id}")
async def get_progress(user_id: str):
    """Get user progress"""
    if user_id not in progress_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    return progress_db[user_id]


# Roadmap endpoints
@app.get("/api/roadmap/{user_id}")
async def get_roadmap(user_id: str):
    """Get personalized roadmap"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    from agent.roadmap import RoadmapPlanner
    
    user = users_db[user_id]
    level = user.get("level", "Beginner")
    
    planner = RoadmapPlanner(level)
    
    return {
        "user_id": user_id,
        "level": level,
        "roadmap": planner.get_roadmap()
    }


# Stats endpoints
@app.get("/api/stats/{user_id}")
async def get_stats(user_id: str):
    """Get user statistics"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    user = users_db[user_id]
    progress = progress_db.get(user_id, {})
    
    return {
        "user_id": user_id,
        "username": user.get("username", ""),
        "level": user.get("level", "Beginner"),
        "topics_covered": len(progress.get("topics_covered", [])),
        "problems_attempted": progress.get("problems_attempted", 0),
        "weak_topics": progress.get("weak_topics", [])
    }


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

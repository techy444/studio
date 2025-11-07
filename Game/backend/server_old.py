from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import our modules
from database import db, users_collection, battles_collection
from auth_utils import verify_password, get_password_hash, create_access_token, verify_token

app = FastAPI(title="CodeDuel Arena API")

# NOTE: `server_old.py` is deprecated. It contains legacy/experimental endpoints
# that rely on a private package (`emergentintegrations`) and is kept for
# reference only. Prefer `server.py` for the current API surface. Consider
# moving this file to `backend/legacy/` or removing it from installs.

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:9002"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()

# Pydantic Models
class SignupRequest(BaseModel):
    username: str
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: dict

class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    created_at: str
    total_points: int
    wins: int
    losses: int

class BattleTimeoutRequest(BaseModel):
    battle_id: str
    winner_id: Optional[str] = None

# Helper function to get current user from token
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id = payload.get("sub")
    user = users_collection.find_one({"_id": user_id})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    return user

@app.get("/")
async def root():
    return {"message": "CodeDuel Arena API", "status": "running"}

@app.post("/api/auth/signup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def signup(request: SignupRequest):
    """
    Register a new user
    """
    # Check if email already exists
    if users_collection.find_one({"email": request.email}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Check if username already exists
    if users_collection.find_one({"username": request.username}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Create user
    import uuid
    user_id = str(uuid.uuid4())
    hashed_password = get_password_hash(request.password)
    
    user_data = {
        "_id": user_id,
        "username": request.username,
        "email": request.email,
        "hashed_password": hashed_password,
        "created_at": datetime.utcnow().isoformat(),
        "total_points": 0,
        "wins": 0,
        "losses": 0
    }
    
    users_collection.insert_one(user_data)
    
    # Create access token
    access_token = create_access_token(data={"sub": user_id})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user_id,
            "username": request.username,
            "email": request.email,
            "total_points": 0,
            "wins": 0,
            "losses": 0
        }
    }

@app.post("/api/auth/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    """
    Login user and return JWT token
    """
    # Find user by email
    user = users_collection.find_one({"email": request.email})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Verify password
    if not verify_password(request.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Create access token
    access_token = create_access_token(data={"sub": user["_id"]})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user["_id"],
            "username": user["username"],
            "email": user["email"],
            "total_points": user.get("total_points", 0),
            "wins": user.get("wins", 0),
            "losses": user.get("losses", 0)
        }
    }

@app.get("/api/auth/me", response_model=UserResponse)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """
    Get current user information from JWT token
    """
    return {
        "id": current_user["_id"],
        "username": current_user["username"],
        "email": current_user["email"],
        "created_at": current_user["created_at"],
        "total_points": current_user.get("total_points", 0),
        "wins": current_user.get("wins", 0),
        "losses": current_user.get("losses", 0)
    }

@app.post("/api/battle/timeout")
async def battle_timeout(request: BattleTimeoutRequest, current_user: dict = Depends(get_current_user)):
    """
    Handle battle timeout
    """
    battle_data = {
        "battle_id": request.battle_id,
        "status": "timeout",
        "end_time": datetime.utcnow().isoformat(),
        "winner_id": request.winner_id
    }
    
    # Update or insert battle
    battles_collection.update_one(
        {"battle_id": request.battle_id},
        {"$set": battle_data},
        upsert=True
    )
    
    return {"message": "Battle ended due to timeout", "battle": battle_data}

@app.post("/api/battle/start")
async def start_battle(current_user: dict = Depends(get_current_user)):
    """
    Start a new battle
    """
    import uuid
    battle_id = str(uuid.uuid4())
    
    battle_data = {
        "battle_id": battle_id,
        "start_time": datetime.utcnow().isoformat(),
        "status": "active",
        "player1_id": current_user["_id"],
        "player2_id": None  # Will be filled when opponent joins
    }
    
    battles_collection.insert_one(battle_data)
    
    return {"message": "Battle started", "battle_id": battle_id}

class CodeExplainerRequest(BaseModel):
    code_snippet: str

@app.post("/api/explainer/explain")
async def explain_code(request: CodeExplainerRequest):
    """
    Explain code snippet using AI
    """
    try:
        from emergentintegrations.llm.chat import LlmChat, UserMessage
        import uuid
        
        # Initialize chat with Emergent LLM key
        chat = LlmChat(
            api_key=os.getenv("EMERGENT_LLM_KEY"),
            session_id=str(uuid.uuid4()),
            system_message="You are a senior engineer explaining code line by line. Identify and explain any relevant programming paradigms such as dependency injection, design patterns, and best practices."
        ).with_model("gemini", "gemini-2.0-flash")
        
        # Create user message
        user_message = UserMessage(
            text=f"Explain the following code snippet line by line:\n\n```\n{request.code_snippet}\n```"
        )
        
        # Get explanation
        explanation = await chat.send_message(user_message)
        
        return {"explanation": explanation}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to explain code: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
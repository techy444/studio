from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime, timedelta
import os
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import our modules
from database import db, users_collection, battles_collection, problems_collection
from auth_utils import verify_password, get_password_hash, create_access_token, verify_token
from pymongo.errors import DuplicateKeyError
from typing import List

app = FastAPI(title="CodeDuel Arena API")

# CORS Configuration - Updated to include port 9002
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:9002", "http://localhost:8001"],
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
    name: Optional[str] = None
    gemini_api_key: Optional[str] = None

class ProfileUpdateRequest(BaseModel):
    name: Optional[str] = None
    gemini_api_key: Optional[str] = None

class BattleTimeoutRequest(BaseModel):
    battle_id: str
    winner_id: Optional[str] = None

class CodeExplainerRequest(BaseModel):
    code_snippet: str
    language: Optional[str] = "python"  # Default to Python if not specified

class ProblemFilter(BaseModel):
    difficulty: Optional[str] = None
    category: Optional[str] = None
    search: Optional[str] = None

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
        "losses": 0,
        "name": None,
        "gemini_api_key": None
    }
    
    try:
        users_collection.insert_one(user_data)
    except DuplicateKeyError:
        # Race condition: another request inserted the same email/username
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email or username already exists"
        )
    
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
            "losses": 0,
            "name": None,
            "gemini_api_key": None
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
            "losses": user.get("losses", 0),
            "name": user.get("name"),
            "gemini_api_key": user.get("gemini_api_key")
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
        "losses": current_user.get("losses", 0),
        "name": current_user.get("name"),
        "gemini_api_key": current_user.get("gemini_api_key")
    }

@app.get("/api/profile")
async def get_profile(current_user: dict = Depends(get_current_user)):
    """
    Get user profile information
    """
    return {
        "id": current_user["_id"],
        "username": current_user["username"],
        "email": current_user["email"],
        "name": current_user.get("name"),
        "gemini_api_key": current_user.get("gemini_api_key"),
        "total_points": current_user.get("total_points", 0),
        "wins": current_user.get("wins", 0),
        "losses": current_user.get("losses", 0),
        "created_at": current_user.get("created_at")
    }

@app.put("/api/profile")
async def update_profile(
    profile: ProfileUpdateRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Update user profile (name, gemini_api_key, etc.)
    """
    update_data = {}
    
    if profile.name is not None:
        update_data["name"] = profile.name
    
    if profile.gemini_api_key is not None:
        update_data["gemini_api_key"] = profile.gemini_api_key
    
    if update_data:
        users_collection.update_one(
            {"_id": current_user["_id"]},
            {"$set": update_data}
        )
    
    # Fetch updated user
    updated_user = users_collection.find_one({"_id": current_user["_id"]})
    
    return {
        "message": "Profile updated successfully",
        "user": {
            "id": updated_user["_id"],
            "username": updated_user["username"],
            "email": updated_user["email"],
            "name": updated_user.get("name"),
            "gemini_api_key": updated_user.get("gemini_api_key"),
            "total_points": updated_user.get("total_points", 0),
            "wins": updated_user.get("wins", 0),
            "losses": updated_user.get("losses", 0)
        }
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


@app.get("/api/problems")
async def get_problems(
    difficulty: Optional[str] = None,
    category: Optional[str] = None,
    search: Optional[str] = None
):
    """
    Get all problems with optional filtering
    """
    query = {}
    
    if difficulty:
        query["difficulty"] = difficulty
    
    if category:
        query["category"] = category
    
    if search:
        query["$or"] = [
            {"title": {"$regex": search, "$options": "i"}},
            {"description": {"$regex": search, "$options": "i"}}
        ]
    
    problems = list(problems_collection.find(query))
    
    # Convert MongoDB _id to string and rename to id
    for problem in problems:
        problem["id"] = problem.pop("problem_id")
        problem.pop("_id", None)
    
    return {"problems": problems, "count": len(problems)}

@app.get("/api/problems/{problem_id}")
async def get_problem(problem_id: str):
    """
    Get a specific problem by ID
    """
    problem = problems_collection.find_one({"problem_id": problem_id})
    
    if not problem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Problem not found"
        )
    
    problem["id"] = problem.pop("problem_id")
    problem.pop("_id", None)
    
    return problem


@app.post("/api/explainer/explain")
async def explain_code(request: CodeExplainerRequest, current_user: dict = Depends(get_current_user)):
    """
    Explain code snippet using Gemini AI with retry logic
    """
    # Limit the size of the snippet to avoid accidental/excessive LLM usage
    if not request.code_snippet or len(request.code_snippet) > 5000:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Code snippet too long (max 5000 characters)"
        )
    # Check if user has configured Gemini API key
    gemini_api_key = current_user.get("gemini_api_key")
    if not gemini_api_key:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please configure your Gemini API key in your profile settings"
        )
    
    max_retries = 3
    retry_delay = 2  # seconds
    
    for attempt in range(max_retries):
        try:
            import google.generativeai as genai
            
            # Configure Gemini
            genai.configure(api_key=gemini_api_key)
            
            # Use gemini-2.5-flash model as requested
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            # Create prompt
            language = request.language or "Python"
            prompt = f"""You are a senior engineer explaining {language} code line by line. 
Identify and explain any relevant programming paradigms such as dependency injection, 
design patterns, and best practices.

Please explain the following {language} code snippet in detail:

```{language.lower()}
{request.code_snippet}
```

Provide a clear, line-by-line explanation."""
            
            # Generate explanation
            response = model.generate_content(prompt)
            
            if response.text:
                return {
                    "explanation": response.text,
                    "success": True
                }
            else:
                raise Exception("Empty response from Gemini API")
                
        except Exception as e:
            error_msg = str(e)
            
            # Check for specific error types
            if "API_KEY_INVALID" in error_msg or "invalid api key" in error_msg.lower():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid Gemini API key. Please update your API key in profile settings."
                )
            
            # If this is the last attempt, raise the error
            if attempt == max_retries - 1:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Failed to explain code after {max_retries} attempts: {error_msg}"
                )
            
            # Wait before retrying
            time.sleep(retry_delay)
            retry_delay *= 2  # Exponential backoff
    
    # Should never reach here, but just in case
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Failed to explain code"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

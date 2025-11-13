from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from services.user_service import authenticate_user, create_user

router = APIRouter(prefix="/auth", tags=["Auth"])  # CHANGE THIS

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class SignupRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str = "user"

# LOGIN
@router.post("/login")
async def login(data: LoginRequest):
    user = await authenticate_user(data.email, data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"user": {"username": user.username, "email": user.email, "role": user.role}}

# SIGNUP
@router.post("/signup")
async def signup(data: SignupRequest):
    try:
        user = await create_user(data.dict())
        return {"user": {"username": user.username, "email": user.email, "role": user.role}}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
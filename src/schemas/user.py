from pydantic import BaseModel, EmailStr
from typing import Optional, Literal
from datetime import datetime

# Add this missing schema
class UserProfile(BaseModel):
    username: str
    email: EmailStr
    role: Literal["user", "admin"] = "user"
    profile_picture: Optional[str] = None
    bio: Optional[str] = None
    created_at: datetime

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: Literal["user", "admin"] = "user"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    role: str
    created_at: datetime
    profile_picture: Optional[str] = None
    bio: Optional[str] = None
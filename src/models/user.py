from beanie import Document
from pydantic import EmailStr
from typing import Literal, Optional
from datetime import datetime

class User(Document):
    username: str
    email: EmailStr
    password: str
    role: Literal["user", "admin"] = "user"
    created_at: datetime = datetime.utcnow()
    profile_picture: Optional[str] = None
    bio: Optional[str] = None

    class Settings:
        name = "users"
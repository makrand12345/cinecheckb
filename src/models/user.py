from beanie import Document
from pydantic import EmailStr
from typing import Literal, Optional, List
from datetime import datetime
from beanie import PydanticObjectId

class User(Document):
    username: str
    email: EmailStr
    password: str
    role: Literal["user", "admin"] = "user"
    created_at: datetime = datetime.utcnow()
    profile_picture: Optional[str] = None
    bio: Optional[str] = None
    watchlist: List[PydanticObjectId] = []  # List of movie IDs

    class Settings:
        name = "users"
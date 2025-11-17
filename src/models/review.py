from beanie import Document
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from beanie import PydanticObjectId

class Review(Document):
    movie_id: PydanticObjectId
    user_id: str  # email or user id
    username: str
    rating: int  # 1-5 stars
    review_text: Optional[str] = None
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()
    
    class Settings:
        name = "reviews"
        indexes = ["movie_id", "user_id"]


from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ReviewCreate(BaseModel):
    movie_id: str
    rating: int  # 1-5
    review_text: Optional[str] = None
    user_id: Optional[str] = None  # Will be set from session/auth in future
    username: Optional[str] = None

class ReviewOut(BaseModel):
    id: str
    movie_id: str
    user_id: str
    username: str
    rating: int
    review_text: Optional[str] = None
    created_at: datetime
    updated_at: datetime


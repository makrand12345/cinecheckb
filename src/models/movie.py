from beanie import Document
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class CastMember(BaseModel):
    name: str
    role: str

class Movie(Document):
    title: str
    description: str
    genres: List[str] = []
    release_date: Optional[str] = None
    duration: Optional[int] = None
    poster_url: Optional[str] = None
    trailer_url: Optional[str] = None
    director: Optional[str] = None
    cast: List[CastMember] = []
    language: Optional[str] = None
    country: Optional[str] = None
    age_rating: Optional[str] = None
    rating: Optional[float] = None
    submitted_by: Optional[str] = None
    status: str = "pending"
    featured: bool = False
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()

    class Settings:
        name = "movies"
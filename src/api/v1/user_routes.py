from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional, Literal
from datetime import datetime
from services.user_service import get_user

router = APIRouter(prefix="/users", tags=["Users"])  # CHANGE THIS

class UserProfileResponse(BaseModel):
    username: str
    email: EmailStr
    role: Literal["user", "admin"]
    profile_picture: Optional[str] = None
    bio: Optional[str] = None
    created_at: datetime

@router.get("/{user_id}", response_model=UserProfileResponse)
async def get_user_profile(user_id: str):
    user = await get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserProfileResponse(
        username=user.username,
        email=user.email,
        role=user.role,
        profile_picture=user.profile_picture,
        bio=user.bio,
        created_at=user.created_at
    )

@router.put("/{user_id}")
async def update_user_profile(user_id: str, profile_data: UserProfileResponse):
    user = await get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.username = profile_data.username
    user.bio = profile_data.bio
    user.profile_picture = profile_data.profile_picture
    return {"message": "Profile updated successfully"}

from typing import Optional, Dict, Any
from models.user import User

async def create_user(user_data: Dict[str, Any]) -> User:
    # Check if user already exists in MongoDB
    existing_user = await User.find_one({"email": user_data["email"]})
    if existing_user:
        raise ValueError("User with this email already exists")
    
    # Create new user in MongoDB
    user = User(
        username=user_data["username"],
        email=user_data["email"],
        password=user_data["password"],
        role=user_data.get("role", "user")
    )
    await user.insert()
    return user

async def authenticate_user(email: str, password: str) -> Optional[User]:
    user = await User.find_one({"email": email})
    if user and user.password == password:
        return user
    return None

async def get_user(user_id: str) -> Optional[User]:
    return await User.find_one({"email": user_id})
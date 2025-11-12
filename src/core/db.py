from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from src.models.movie import Movie
from src.models.user import User  # if you have User model
from src.core.config import settings

async def init_db():
    client = AsyncIOMotorClient(settings.MONGODB_URI)
    db = client[settings.DB_NAME]
    await init_beanie(database=db, document_models=[Movie, User])

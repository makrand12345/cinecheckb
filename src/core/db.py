import certifi
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from core.config import settings
from models.movie import Movie
from models.user import User

async def init_db():
    client = AsyncIOMotorClient(
        settings.MONGODB_URI,
        tls=True,
        tlsCAFile=certifi.where()  # ensure proper SSL verification
    )
    db = client[settings.DB_NAME]
    await init_beanie(database=db, document_models=[Movie, User])

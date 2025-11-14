from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from models.movie import Movie
from models.user import User
from core.config import settings

async def init_db():
    client = AsyncIOMotorClient(
        settings.MONGODB_URI,
        tls=True,
        tlsAllowInvalidCertificates=True,
        tlsInsecure=True        # <-- FIX FOR RENDER
    )

    db = client[settings.DB_NAME]

    await init_beanie(
        database=db,
        document_models=[Movie, User]
    )

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from models.movie import Movie
from models.user import User
from core.config import settings
import ssl

async def init_db():
    # MongoDB Atlas requires SSL
    client = AsyncIOMotorClient(
        settings.MONGODB_URI,
        tls=True,
        tlsAllowInvalidCertificates=True
    )

    db = client[settings.DB_NAME]
    await init_beanie(database=db, document_models=[Movie, User])

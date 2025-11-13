from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from models.movie import Movie
from models.user import User
from core.config import settings
import ssl

async def init_db():
    # Create SSL context
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    client = AsyncIOMotorClient(
        settings.MONGODB_URI,
        tls=True,
        tlsInsecure=True,  # Allow insecure TLS
        ssl=ssl_context
    )
    db = client[settings.DB_NAME]
    await init_beanie(database=db, document_models=[Movie, User])
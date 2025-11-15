import certifi
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from core.config import settings
from models.movie import Movie
from models.user import User

async def init_db():
    """
    Initialize MongoDB connection with Beanie.
    Handles SSL/TLS for MongoDB Atlas connections.
    """
    mongodb_uri = settings.MONGODB_URI
    
    # For mongodb+srv:// connections, MongoDB Atlas handles SSL/TLS automatically
    # Don't specify tlsCAFile as it can cause SSL handshake conflicts
    # The system's default CA certificates will be used
    if mongodb_uri.startswith("mongodb+srv://"):
        # SRV connections: SSL/TLS is automatic, use default system certs
        client = AsyncIOMotorClient(mongodb_uri)
    else:
        # Standard mongodb:// connections: explicitly enable TLS with certifi
        client = AsyncIOMotorClient(
            mongodb_uri,
            tls=True,
            tlsCAFile=certifi.where()
        )
    
    # Test the connection
    try:
        await client.admin.command('ping')
        db = client[settings.DB_NAME]
        await init_beanie(database=db, document_models=[Movie, User])
        print("✅ MongoDB connected and Beanie initialized")
    except Exception as e:
        print(f"❌ MongoDB connection error: {e}")
        print(f"   Connection URI format: {'mongodb+srv://' if mongodb_uri.startswith('mongodb+srv://') else 'mongodb://'}")
        raise

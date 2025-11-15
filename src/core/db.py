import certifi
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from core.config import settings
from models.movie import Movie
from models.user import User

async def init_db():
    """
    Initialize MongoDB connection with Beanie.
    Uses certifi for SSL certificate validation with MongoDB Atlas.
    """
    # MongoDB Atlas connection handling
    # mongodb+srv:// connections automatically use SSL/TLS
    # We provide certifi CA certificates for proper validation
    mongodb_uri = settings.MONGODB_URI
    
    # For mongodb+srv://, SSL is automatic, just need CA certs
    # For mongodb://, we may need to explicitly enable TLS
    if mongodb_uri.startswith("mongodb+srv://"):
        # SRV connections automatically use TLS, just provide CA certs
        client = AsyncIOMotorClient(
            mongodb_uri,
            tlsCAFile=certifi.where()
        )
    else:
        # Standard connection - enable TLS explicitly
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
    except Exception as e:
        print(f"❌ MongoDB connection error: {e}")
        raise

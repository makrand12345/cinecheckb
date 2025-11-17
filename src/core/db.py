import certifi
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from core.config import settings
from models.movie import Movie
from models.user import User
from models.review import Review

async def init_db():
    """
    Initialize MongoDB connection with Beanie.
    Handles SSL/TLS for MongoDB Atlas connections.
    """
    mongodb_uri = settings.MONGODB_URI
    
    if not mongodb_uri:
        raise ValueError("MONGODB_URI environment variable is not set")
    
    print(f"🔌 Connecting to MongoDB...")
    print(f"   URI format: {'mongodb+srv://' if mongodb_uri.startswith('mongodb+srv://') else 'mongodb://'}")
    print(f"   Database: {settings.DB_NAME}")
    
    # For mongodb+srv:// connections, MongoDB Atlas handles SSL/TLS automatically
    # Don't specify tlsCAFile as it can cause SSL handshake conflicts
    # The system's default CA certificates will be used
    try:
        if mongodb_uri.startswith("mongodb+srv://"):
            # SRV connections: SSL/TLS is automatic, use default system certs
            # Add connection timeout and server selection timeout
            client = AsyncIOMotorClient(
                mongodb_uri,
                serverSelectionTimeoutMS=10000,  # 10 seconds
                connectTimeoutMS=10000
            )
        else:
            # Standard mongodb:// connections: explicitly enable TLS with certifi
            client = AsyncIOMotorClient(
                mongodb_uri,
                tls=True,
                tlsCAFile=certifi.where(),
                serverSelectionTimeoutMS=10000,
                connectTimeoutMS=10000
            )
        
        # Test the connection
        print("   Testing connection...")
        await client.admin.command('ping')
        print("   ✅ Connection successful!")
        
        db = client[settings.DB_NAME]
        await init_beanie(database=db, document_models=[Movie, User, Review])
        print("✅ MongoDB connected and Beanie initialized")
        
    except Exception as e:
        error_msg = str(e)
        print(f"❌ MongoDB connection error: {error_msg}")
        
        # Provide helpful troubleshooting information
        if "SSL handshake failed" in error_msg or "TLSV1_ALERT" in error_msg:
            print("\n🔧 Troubleshooting SSL/TLS errors:")
            print("   1. Check MongoDB Atlas Network Access:")
            print("      - Go to MongoDB Atlas → Network Access")
            print("      - Add IP address: 0.0.0.0/0 (allow from anywhere)")
            print("      - Or add Render's specific IP ranges")
            print("   2. Verify your connection string format:")
            print("      - Should be: mongodb+srv://username:password@cluster.mongodb.net/")
            print("      - Ensure username/password are URL-encoded if they contain special chars")
            print("   3. Check database user permissions in MongoDB Atlas")
        
        raise

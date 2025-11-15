from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router as api_router
from core.db import init_db
from core.config import settings
import os

app = FastAPI(title="CineCheck API")

# Enable CORS for frontend
# Get CORS origins from environment or settings
cors_origins_env = os.getenv("CORS_ORIGINS")
if cors_origins_env:
    cors_origins = [origin.strip() for origin in cors_origins_env.split(",") if origin.strip()]
else:
    cors_origins = settings.CORS_ORIGINS if isinstance(settings.CORS_ORIGINS, list) else [settings.CORS_ORIGINS]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix="/api/v1")

# Lifespan startup event
@app.on_event("startup")  # Render will still call this
async def startup_event():
    try:
        await init_db()
        print("✅ MongoDB connected and Beanie initialized")
    except Exception as e:
        print(f"❌ MongoDB failed: {e}")


@app.get("/")
def root():
    return {"message": "CineCheck API is running!"}

# Run on Render
if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

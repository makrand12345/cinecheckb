from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router as api_router
from core.db import init_db
from core.config import settings

app = FastAPI(title="CineCheck API")

# Enable CORS for Angular frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix="/api/v1")

# Startup event to init DB
@app.on_event("startup")
async def on_startup():
    try:
        await init_db()
        print("✅ MongoDB connected and Beanie initialized")
    except Exception as e:
        print(f"❌ MongoDB failed: {e}")

@app.get("/")
def root():
    return {"message": "CineCheck API is running!"}
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router as api_router
from core.db import init_db
from core.config import settings

app = FastAPI(title="CineCheck API")

# Enable CORS for Angular frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://cinecheckf.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix="/api/v1")

# ✅ ENABLE DATABASE CONNECTION
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

# For Render deployment
import os
import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
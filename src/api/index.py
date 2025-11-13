from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import router as api_router
from src.core.config import settings

app = FastAPI(title="CineCheck API")

# Enable CORS for Angular frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "CineCheck API is running!"}

# Vercel serverless function handler
async def handler(request, response):
    # This makes FastAPI compatible with Vercel's serverless environment
    from mangum import Mangum
    handler = Mangum(app)
    return await handler(request, response)
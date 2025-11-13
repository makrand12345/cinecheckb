from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router as api_router

app = FastAPI(title="CineCheck API")

# Enable CORS for your Angular frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://cinecheckf.vercel.app",
        "http://localhost:4200"  # For local development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "CineCheck API is running!"}

# For Render deployment
import os
import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
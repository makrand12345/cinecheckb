from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS with explicit response headers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "MINIMAL ROOT WORKS"}

@app.get("/test")
def test():
    return {"message": "MINIMAL TEST WORKS"}

@app.post("/signup")
def signup():
    return {"message": "MINIMAL SIGNUP WORKS"}

print("🎯 MINIMAL APP READY!")
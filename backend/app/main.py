from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow your React frontend to communicate with this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Backend is running!"}

@app.get("/api/projects")
def get_projects():
    return [
        {
            "id": 1,
            "name": "RepoPilot AI", 
            "description": "Production-oriented codebase intelligence platform."
        },
        {
            "id": 2,
            "name": "Voice Notes AI", 
            "description": "Local-first AI application for audio transcription."
        }
    ]
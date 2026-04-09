from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.agent import run_agent

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://ai-travel-agent-omega.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    message: str
    user_id: str = "default"

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.post("/chat")
def chat(query: Query):
    try:
        response = run_agent(query.message, query.user_id)
        return {"response": response}
    except Exception as e:
        return {
            "response": "Sorry, the AI service is currently unavailable. Please try again later."
        }
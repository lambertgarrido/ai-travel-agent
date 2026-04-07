from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

class Query(BaseModel):
    message: str
    user_id: str = "default"

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://ai-travel-agent-omega.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
def chat(query: Query):
    response = run_agent(query.message, query.user_id)
    return {"response": response}
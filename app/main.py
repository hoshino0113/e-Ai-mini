from fastapi import FastAPI
from pydantic import BaseModel
from app.llm_client import OllamaClient


app = FastAPI(title="Enterprise AI Agent")

llm = OllamaClient(model="deepseek-r1:14b")


class AskRequest(BaseModel):
    question: str


@app.get("/")
def health_check():
    return {"status": "running"}


@app.post("/ask")
def ask(request: AskRequest):
    decision = llm.decide_tool(request.question)

    return {
        "question": request.question,
        "decision": decision
    }
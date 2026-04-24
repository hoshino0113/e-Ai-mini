from fastapi import FastAPI
from pydantic import BaseModel
from app.llm_client import OllamaClient
from app.tools.sql_tool import query_sql

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

    tool_name = decision.get("tool")
    tool_input = decision.get("input", request.question)

    if tool_name == "query_sql":
        tool_result = query_sql(tool_input)
    else:
        tool_result = {
            "status": "skipped",
            "message": f"No tool executed for tool: {tool_name}"
        }

    return {
        "question": request.question,
        "decision": decision,
        "tool_result": tool_result
    }
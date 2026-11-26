import httpx
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field
from app import llm
import ollama

app = FastAPI(title="Mini RAG")

@app.get("/health")
def health():
    return {"status": "ok"}

class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)


class AskResponse(BaseModel):
    answer: str
    
@app.post("/ask", response_model=AskResponse)
async def ask(request: AskRequest):
    try:
        answer = await llm.generate(request.question)
    except (ConnectionError, ollama.ResponseError):
        raise HTTPException(status_code=502, detail="The model service failed.")
    return AskResponse(answer=answer)
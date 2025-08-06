# routers/query.py
from fastapi import APIRouter, Request
from pydantic import BaseModel
from deps import limiter
from openai_wrapper import get_answer, get_embedding
from utils import build_prompt

router = APIRouter()

class QuestionRequest(BaseModel):
    question: str

@router.post("/query")
@limiter.limit("5/hour")
async def query_rag(request: Request, body: QuestionRequest):
    q_vec = get_embedding(body.question)
    hits = request.app.state.qdrant_client.search(
        collection_name="rag_documents",
        query_vector=q_vec,
        limit=3
    )
    contexts = [h.payload["text"] for h in hits]
    prompt   = build_prompt(contexts, body.question)
    answer   = get_answer(prompt)
    return {
        "answer":  answer,
        "sources": [h.payload["source"] for h in hits]
    }

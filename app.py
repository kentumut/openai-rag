from fastapi import FastAPI, Request
from pydantic import BaseModel
from openai_wrapper import get_answer, get_embedding
from utils import build_prompt
from qdrant_client import QdrantClient
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

COLLECTION_NAME = "rag_documents"
client = QdrantClient(path="./qdrant_data")

app.add_middleware(SlowAPIMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["kentumut.com"],  # You can restrict this to ["http://localhost:3000"] etc.
    allow_credentials=True,
    allow_methods=["*"],  # Or ["POST"] specifically
    allow_headers=["*"],
)
class QuestionRequest(BaseModel):
    question: str

@app.post("/query")
@limiter.limit("5/hour")
def query_rag(request: QuestionRequest, req: Request):
    query_embedding = get_embedding(request.question)
    search_result = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_embedding,
        limit=3
    )

    contexts = [hit.payload['text'] for hit in search_result]
    prompt = build_prompt(contexts, request.question)
    answer = get_answer(prompt)
    return {
        "answer": answer,
        "sources": [hit.payload['source'] for hit in search_result]
    }

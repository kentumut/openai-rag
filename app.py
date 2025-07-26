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

app = FastAPI(
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(SlowAPIMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
      "https://kentumut.com",
      "https://www.kentumut.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

COLLECTION_NAME = "rag_documents"
client = QdrantClient(path="./qdrant_data")

class QuestionRequest(BaseModel):
    question: str

@app.post("/query")
@limiter.limit("5/hour")
def query_rag(request: Request, body: QuestionRequest):
    # Now `request` is the starlette.requests.Request…
    # and `body` is your parsed JSON.
    query_embedding = get_embedding(body.question)
    search_result = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_embedding,
        limit=3
    )

    contexts = [hit.payload['text'] for hit in search_result]
    prompt   = build_prompt(contexts, body.question)
    answer   = get_answer(prompt)

    return {
        "answer": answer,
        "sources": [hit.payload['source'] for hit in search_result]
    }

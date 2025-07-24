from fastapi import FastAPI
from pydantic import BaseModel
from openai_wrapper import get_answer, get_embedding
from utils import build_prompt
from qdrant_client import QdrantClient

app = FastAPI()
COLLECTION_NAME = "rag_documents"
client = QdrantClient(path="./qdrant_data")

class QuestionRequest(BaseModel):
    question: str

@app.post("/query")
def query_rag(request: QuestionRequest):
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

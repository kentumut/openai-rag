from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
import os

COLLECTION_NAME = "rag_documents"

client = QdrantClient(path="./qdrant_data")

def create_collection(vector_size: int):
    if not client.collection_exists(COLLECTION_NAME):
        client.recreate_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
        )

def get_qdrant_client():
    return client

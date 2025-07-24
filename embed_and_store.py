from openai_wrapper import get_embedding
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from utils import load_documents
import uuid

COLLECTION_NAME = "rag_documents"

client = QdrantClient(path="./qdrant_data")
client.recreate_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
)

documents = load_documents("data")
points = []

for file_name, text in documents:
    embedding = get_embedding(text)
    points.append(PointStruct(
        id=str(uuid.uuid4()),
        vector=embedding,
        payload={"text": text, "source": file_name}
    ))

client.upsert(collection_name=COLLECTION_NAME, points=points)
print("All documents embedded and stored.")

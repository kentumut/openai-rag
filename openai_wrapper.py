import os
import openai
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()
def get_embedding(text: str) -> list[float]:
    res = client.embeddings.create(
        model="text-embedding-ada-002",
        input=text
    )
    return res.data[0].embedding

def get_answer(prompt: str) -> str:
    messages = [{"role": "user", "content": prompt}]
    response = client.responses.create(
        model="gpt-3.5-turbo",
        input=messages,
        temperature=0.0
    )
    return response.output_text

import os

def load_documents(folder="data"):
    docs = []
    for file in os.listdir(folder):
        if file.endswith(".txt"):
            path = os.path.join(folder, file)
            with open(path, "r", encoding="utf-8") as f:
                docs.append((file, f.read()))
    return docs

def build_prompt(contexts: list[str], question: str) -> str:
    joined_context = "\n\n".join(contexts)
    return f"""Use the following context to answer the question.
    Context:
    {joined_context}
    Question: {question}
    Answer:"""

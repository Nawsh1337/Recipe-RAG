from fastapi import FastAPI
from pydantic import BaseModel
import chromadb
import ollama
import yaml

app = FastAPI()

with open("C:/Users/HP/Desktop/Recipe-RAG/config.yaml", "r") as f:
    config = yaml.safe_load(f)

chroma_client = chromadb.PersistentClient(path="C:/Users/HP/Desktop/Recipe-RAG/data/chroma_db")
collection = chroma_client.get_collection(name="recipes")
EMBEDDING_MODEL = config['models']['embedding_model']
LANGUAGE_MODEL = config['models']['language_model']

class Query(BaseModel):
    query: str
    n_docs: int = 3

@app.post("/retrieve")
def retrieve(query_obj: Query):
    query_embedding = ollama.embed(model=EMBEDDING_MODEL, input=query_obj.query)['embeddings'][0]
    results = collection.query(query_embeddings=[query_embedding], n_results=query_obj.n_docs)

    return {
        "results": [
            {"document": doc, "title": meta["title"]}
            for doc, meta in zip(results["documents"][0], results["metadatas"][0])
        ]
    }

@app.post("/chat")
def chat(prompt: Query):
    instruction_prompt = "You are a helpful assistant for recipes."
    messages = [{'role': 'system', 'content': instruction_prompt}]
    messages = [
        {"role": "system", "content": instruction_prompt},
        {"role": "user", "content": prompt.query}
    ]
    response = ollama.chat(model=LANGUAGE_MODEL, messages=messages)
    return {"response": response['message']['content']}

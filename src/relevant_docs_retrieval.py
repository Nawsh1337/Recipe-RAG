import yaml
import ollama
# import chromadb
import os
import requests


def retrieve(query,n_docs=5):
    # client = chromadb.PersistentClient(path="data/chroma_db")
    # collection = client.get_collection(name="recipes")

    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    
    OLLAMA_HOST = config.get('ollama_host')
    if OLLAMA_HOST:
        os.environ["OLLAMA_HOST"] = OLLAMA_HOST

    # EMBEDDING_MODEL = config['models']['embedding_model']
    query = "sweet dish with egg"
    # query_embedding = ollama.embed(model=EMBEDDING_MODEL, input=query)['embeddings'][0]

    res = requests.post("https://3037-104-151-16-103.ngrok-free.app/retrieve", json={"query": query, "n_docs": 3})
    return res.json()["results"]

    # res = {}#top 5 relevant documents
    # for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
    #     res[doc] = meta["title"]
    # return res
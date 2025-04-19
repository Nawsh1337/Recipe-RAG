import yaml
import ollama
import chromadb

client = chromadb.PersistentClient(path="data/chroma_db")
collection = client.get_collection(name="recipes")

with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)
    
EMBEDDING_MODEL = config['models']['embedding_model']
query = "sweet dish with egg"
query_embedding = ollama.embed(model=EMBEDDING_MODEL, input=query)['embeddings'][0]

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=10
)

for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
    print("🔸", meta["title"])
    print(doc)
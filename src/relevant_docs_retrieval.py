import yaml
import ollama
import chromadb

def retrieve(query,n_docs=5):
    client = chromadb.PersistentClient(path="data/chroma_db")
    collection = client.get_collection(name="recipes")

    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
        
    EMBEDDING_MODEL = config['models']['embedding_model']
    query = "sweet dish with egg"
    query_embedding = ollama.embed(model=EMBEDDING_MODEL, input=query)['embeddings'][0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_docs
    )
    res = {}#top 5 relevant documents
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        res[doc] = meta["title"]
    return res
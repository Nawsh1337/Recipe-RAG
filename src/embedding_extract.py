import ollama
import pandas as pd
import yaml#fancy
import chromadb


df = pd.read_csv('data/recipes_data_cleaned.csv')
df = df.sample(n=200, random_state=42)#100000 too large

with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)
    
EMBEDDING_MODEL = config['models']['embedding_model']

client = chromadb.PersistentClient(path="data/chroma_db")

collection = client.get_or_create_collection(name="recipes")

def add_chunk_to_chroma(chunk, metadata, doc_id):
    embedding = ollama.embed(model=EMBEDDING_MODEL, input=chunk)['embeddings'][0]
    collection.add(
        documents=[chunk],
        embeddings=[embedding],
        metadatas=[metadata],
        ids=[doc_id]
    )

for idx, row in df.iterrows():
    print(idx)
    chunk = f"Title: {row['title']}\nIngredients: {row['ingredients']}\nDirections: {row['directions']}\nNER: {row['NER']}"
    chunk = chunk[:1000]
    metadata = {
        "title": row["title"]
    }
    add_chunk_to_chroma(chunk, metadata, str(idx))

print("ChromaDB saved to disk!")

import yaml
import ollama
# import chromadb
import os
import requests
import json
from datetime import datetime  

def retrieve(query, n_docs=5):
    # Read config
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    
    OLLAMA_HOST = config.get('ollama_host')
    if OLLAMA_HOST:
        os.environ["OLLAMA_HOST"] = OLLAMA_HOST

    # Query example (you can replace this with your own dynamic query if needed)
    query = "sweet dish with egg"

    # Send request to retrieve results
    res = requests.post("https://ab6b-104-151-16-103.ngrok-free.app/retrieve", json={"query": query, "n_docs": n_docs})
    results = res.json().get("results", [])

    # Get current time for the filename
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Save the results to a file named with the current time
    filename = f"{current_time}.json"
    with open(filename, 'w') as f:
        json.dump(results, f, indent=4)

    return results


    # res = {}#top 5 relevant documents
    # for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
    #     res[doc] = meta["title"]
    # return res
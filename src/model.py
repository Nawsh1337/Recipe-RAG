import relevant_docs_retrieval as rdr
import ollama
import yaml
import os
import requests

with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

OLLAMA_HOST = config.get('ollama_host')
if OLLAMA_HOST:
    os.environ["OLLAMA_HOST"] = OLLAMA_HOST

LANGUAGE_MODEL = config['models']['language_model']

instruction_prompt = '''You are a helpful chatbot that provides people names of recipes and how to make them based on the ingredients provided.
Use only the following pieces of context to answer the question, and do NOT provide the NER details. Don't make up any new information:
'''

messages = [{'role': 'system', 'content': instruction_prompt}]

def work(user_query):
    context_lines = rdr.retrieve(user_query, 3)
    context_msg = f"Context:\n{context_lines}"

    messages.append({'role': 'system', 'content': context_msg})
    messages.append({'role': 'user', 'content': user_query})

    stream = requests.post("https://de72-104-151-16-103.ngrok-free.app/chat", json={"query": user_query})
    full_response = ""
    # print(stream.json()["response"])
    for chunk in stream.json()["response"]:
        content = chunk
        full_response += content

    messages.append({'role': 'assistant', 'content': full_response})
    return full_response
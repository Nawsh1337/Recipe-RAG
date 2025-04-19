import relevant_docs_retrieval as rdr
import ollama
import yaml

with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)
    
LANGUAGE_MODEL = config['models']['language_model']

# input_query = input('Ask me a question: ')
# retrieved_knowledge = rdr.retrieve(input_query)

# context_lines = '\n'.join([f' - {key}, {value}' for key, value in retrieved_knowledge.items()])

instruction_prompt = f'''You are a helpful chatbot that provides people names of recipes and how to make them based on the ingredients provided.
Use only the following pieces of context to answer the question, and do NOT provide the NER details. Don't make up any new information:
'''

messages = [{'role': 'system', 'content': instruction_prompt}]


while True:
    user_input = input("\nAsk me a question (or type 'exit'): ")
    if user_input.lower() == 'exit':
        break

    context_lines = rdr.retrieve(user_input,3)
    context_msg = f"Context:\n{context_lines}"

    messages.append({'role': 'system', 'content': context_msg})

    messages.append({'role': 'user', 'content': user_input})

    print("Chatbot response:", end=' ', flush=True)
    stream = ollama.chat(model=LANGUAGE_MODEL, messages=messages, stream=True)

    full_response = ""
    for chunk in stream:
        content = chunk['message']['content']
        print(content, end='', flush=True)
        full_response += content

    messages.append({'role': 'assistant', 'content': full_response})
stream = ollama.chat(
  model=LANGUAGE_MODEL,
  messages=[
    {'role': 'system', 'content': instruction_prompt},
    {'role': 'user', 'content': user_input},
  ],
  stream=True,
)

print('Chatbot response:')
for chunk in stream:
  print(chunk['message']['content'], end='', flush=True)

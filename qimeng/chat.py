import os
import json
import openai

DEFAULT_MODEL = os.environ.get('QIMENG_MODEL', 'gpt-4o')
MEMORY_FILE = os.environ.get('QIMENG_MEMORY_FILE', 'memory.json')


def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def save_memory(memory):
    with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)


def run():
    memory = load_memory()
    print("Welcome to Qimeng. Type 'exit' to quit.")
    while True:
        user_input = input('You: ').strip()
        if user_input.lower() in {'exit', 'quit'}:
            break
        memory.append({'role': 'user', 'content': user_input})
        try:
            response = openai.ChatCompletion.create(
                model=DEFAULT_MODEL,
                messages=memory
            )
            message = response.choices[0].message['content']
        except Exception as e:
            message = f"Error: {e}"
        print(f"Assistant: {message}")
        memory.append({'role': 'assistant', 'content': message})
        save_memory(memory)

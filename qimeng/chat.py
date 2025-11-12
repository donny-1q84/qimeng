import os
import json
import openai
from typing import List, Dict

DEFAULT_MODEL = os.environ.get('QIMENG_MODEL', 'gpt-4o')
MEMORY_FILE = os.environ.get('QIMENG_MEMORY_FILE', 'memory.json')
DEFAULT_SYSTEM_PROMPT = os.environ.get('QIMENG_SYSTEM_PROMPT')

Message = Dict[str, str]


def _ensure_directory_exists(path: str) -> None:
    directory = os.path.dirname(os.path.abspath(path))
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)


def load_memory() -> List[Message]:
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                return []
            if isinstance(data, list):
                return [m for m in data if isinstance(m, dict)]
    return []


def _initialise_system_prompt(memory: List[Message]) -> None:
    if DEFAULT_SYSTEM_PROMPT is None:
        return
    has_system = any(message.get('role') == 'system' for message in memory)
    if not has_system:
        memory.insert(0, {'role': 'system', 'content': DEFAULT_SYSTEM_PROMPT})


def save_memory(memory: List[Message]) -> None:
    _ensure_directory_exists(MEMORY_FILE)
    with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)


def _print_help() -> None:
    print(
        "Available commands:\n"
        "  /help                Show this help message.\n"
        "  /history             Display the current conversation history.\n"
        "  /clear               Clear stored conversation history.\n"
        "  /system <prompt>     Set a custom system prompt for the assistant."
    )


def _display_history(memory: List[Message]) -> None:
    entries = [m for m in memory if m.get('role') != 'system']
    if not entries:
        print("No conversation history yet.")
        return
    for entry in entries:
        role = entry.get('role', 'assistant')
        prefix = 'You' if role == 'user' else 'Assistant'
        print(f"{prefix}: {entry.get('content', '')}")


def _update_system_prompt(memory: List[Message], prompt: str) -> None:
    filtered = [m for m in memory if m.get('role') != 'system']
    if prompt:
        filtered.insert(0, {'role': 'system', 'content': prompt})
    memory[:] = filtered
    save_memory(memory)
    if prompt:
        print("System prompt updated.")
    else:
        print("System prompt removed.")


def handle_command(user_input: str, memory: List[Message]) -> bool:
    if not user_input.startswith('/'):
        return False

    command, _, argument = user_input.partition(' ')
    command = command.lower()

    if command == '/help':
        _print_help()
        return True
    if command == '/history':
        _display_history(memory)
        return True
    if command == '/clear':
        system_messages = [m for m in memory if m.get('role') == 'system']
        memory[:] = system_messages
        save_memory(memory)
        print("Conversation history cleared.")
        return True
    if command == '/system':
        new_prompt = argument.strip()
        _update_system_prompt(memory, new_prompt)
        return True

    print("Unknown command. Type /help for a list of commands.")
    return True


def run():
    memory = load_memory()
    _initialise_system_prompt(memory)
    print("Welcome to Qimeng. Type 'exit' to quit.")
    print("Type /help for available commands.")
    while True:
        user_input = input('You: ').strip()
        if user_input.lower() in {'exit', 'quit'}:
            break
        if handle_command(user_input, memory):
            continue
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

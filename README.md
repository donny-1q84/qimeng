# Qimeng

> An interactive narrative engine for **绮梦** – built with Python and OpenAI's GPT models.

## ✨ Features
- Procedural storylines powered by LLMs
- Memory & character modelling
- Plugin system (custom prompts, tools, vector DB)

## 🚀 Quick start
```bash
pip install -e .
qimeng
```

The `QIMENG_MODEL` environment variable can be used to specify the OpenAI model (default: `gpt-4o`). Conversations are stored in `memory.json` by default.

Set `QIMENG_SYSTEM_PROMPT` to inject a default system message the first time the assistant runs. During a session you can manage the conversation with chat commands:

```
/help                Show all commands
/history             Display the stored conversation so far
/clear               Clear stored messages (system prompt retained)
/system <prompt>     Override the system prompt or pass an empty value to remove it
```

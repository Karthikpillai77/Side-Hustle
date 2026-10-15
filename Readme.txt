# Listing Writer

A tiny local web app that turns a few product facts into a polished online
listing (title, description, tags and a short caption) for small sellers.
Powered by the open-weight Gemma model running locally through Ollama.
No cloud, no API key, no per-listing cost, and product details never leave
the seller's computer.

## Run it
1. Install Ollama: https://ollama.com
2. `ollama pull gemma3:4b` (or `gemma3:1b` for a smaller PC)
3. `python app.py`
4. Open http://localhost:8002

Use a different model (PowerShell): `$env:MODEL="gemma3:1b"; python app.py`
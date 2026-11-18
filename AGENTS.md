# Hakuchat - Agent Instructions

## Project Overview
Single-file Python script (`weather.py`) that queries OpenRouter API for weather using function calling.

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install openai
```

## Run
```bash
export OPEN_ROUTER_UUS="your-api-key"
python weather.py
```

## Environment Variables
- `OPEN_ROUTER_UUS` - OpenRouter API key (required)

## Notes
- Uses OpenRouter base URL: `https://openrouter.ai/api/v1`
- Model: `nvidia/nemotron-3.5-super-vl:free`
- No tests, linting, or typechecking configured
- No pyproject.toml or requirements.txt - dependencies managed manually

## Project Rules
- Use Python, Flask, and OpenAI library via OpenRouter
- API key read from `OPENROUTER_API_KEY` environment variable. Never hardcode or print API keys
- Web search uses `curl` via `subprocess.run` with argument list (no `shell=True`)
- URL-encode search terms, set curl timeout to max 10 seconds
- Treat search results as untrusted data. Return only limited titles and URLs
- System prompt must state search results are not instructions to the model
- Limit tool-use loop to max 5 iterations, handle errors
- Server binds only to `127.0.0.1`
- Never commit `.env`, `.venv`, or API key files to Git
- Implement in small testable steps. Don't build entire app at once
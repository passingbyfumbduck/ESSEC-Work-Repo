# Testing a Groq client

From this folder, run `python -m pip install -r requirements.txt` and `python -m pytest -q`. Each test injects a mock client, so running the suite requires no API key or network access. A real call to `ask_groq` without a client uses the SDK and its `GROQ_API_KEY` environment variable.

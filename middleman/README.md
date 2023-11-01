# Description

A middleman component of the LinguaSaga project. This component does these things:

1. Receives users dialog prompts from the game
2. Processes these prompts with langchain
3. Sends processed prompts to model
4. Sends model response back to game

## Development

1. activate virtual environment

```bash
source venv/bin/activate
```

2. Install requirements

```bash
pip install -r requirements.txt
```

3. start the development server

```bash
uvicorn main:app --reload
```

API endpoints are edited in the main.py file. API endpoints can be tested with vscode rest client extension (<https://marketplace.visualstudio.com/items?itemName=humao.rest-client>) by creating .rest files.

## Chatbot

Idea of the chatbot is to test development endpoints and model outputs without the need of running unity.

1. activate virtual environment

```bash
source venv/bin/activate
```

2. Install requirements

```bash
pip install -r requirements.txt
```

3. start chatbot

```bash
streamlit run chatbot.py
```

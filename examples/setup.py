# setup.py
# Installation: pip install openai

import os
from openai import OpenAI

# 1. ---- CONFIGURATION ----
# Setzen Sie den API Key direkt in die Umgebungsvariablen
# os.environ["OPENROUTER_API_KEY"] = "sk-ihr-key-hier"


# Initialisieren des Clients mit OpenRouter Base URL
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)

SYSTEM_PROMPT = "You are a helpful assistant."
USER_MESSAGE = "Who am I talking to?"
MODEL = "mistralai/mixtral-8x7b-instruct"

# 2. ---- API REQUEST ----
response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": USER_MESSAGE}
    ]
)

# 3. ---- PRINT RESPONSE ----
reply = response.choices[0].message.content
print(reply)

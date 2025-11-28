# For a colab see: https://colab.research.google.com/drive/1-tsUfL2xS9bRr9BxXvoHElxg2eLrUQZi?usp=drive_link

# shell install:
# pip install requests

# Rstudio install (run in R console, after installing reticulate):
# library(reticulate)
# py_install("requests")
# py_install("json")

import requests
import json

# 1. ---- CONFIGURATION ----
# substitute with your api key
API_KEY = "sk-or-v1-f741ccac2597036fc656741122eaf30f1caafe7916fee227a187f9055ff9123"
SYSTEM_PROMPT = "You are a helpful assistant."
USER_MESSAGE = "Who am I talking to?"
MODEL = "mistralai/mixtral-8x7b-instruct"


# 2. ---- API REQUEST ----
response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    },
    json={
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": USER_MESSAGE}
        ]
    }
)

# 3. ---- PRINT RESPONSE ----
reply = response.json()['choices'][0]['message']['content']
print(reply)


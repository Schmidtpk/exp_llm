# Multiple event probability predictions --------------------------

# install required packages within Rstudio
# library(reticulate)
# py_install("pandas")
# py_install("requests")
# py_install("matplotlib")


import os
import pandas as pd
import matplotlib.pyplot as plt
import requests
import json

# Setup API --------------------------

API_KEY = os.environ.get("OPENROUTER_API_KEY")
SYSTEM_PROMPT = "You are an expert forecaster providing probability estimates. Reply with only the requested JSON structure and nothing else."
MODEL = "meta-llama/llama-3.3-70b-instruct"

# Define events --------------------------

events = [
    "Trump will be president in 2028",
    "Global average temperature will increase by more than 1.5°C by 2030",
    "AI will pass the Turing test by 2027",
    "Bitcoin price will exceed $100,000 by end of 2026",
    "Humans will land on Mars by 2035"
]

n = 3

# Run experiment --------------------------

results_list = []

print(f"Sending {len(events) * n} prompts to the LLM...")

for i, event in enumerate(events):
    for j in range(n):
        prompt = (
            f"What is the probability that: {event}? "
            f"Provide your answer as a percentage between 0 and 100. "
            f"If uncertain, you may provide an interval. "
            f"Return a JSON object with three fields: min_prob (minimum probability), prob (point estimate), and max_prob (maximum probability). "
            f"If you have a point estimate with no uncertainty, use the same value for all three fields."
        )

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
                    {"role": "user", "content": prompt}
                ]
            }
        )

        reply = response.json()['choices'][0]['message']['content']

        reply_clean = reply.strip()
        if reply_clean.startswith("```json"):
            reply_clean = reply_clean[7:]
        if reply_clean.startswith("```"):
            reply_clean = reply_clean[3:]
        if reply_clean.endswith("```"):
            reply_clean = reply_clean[:-3]
        reply_clean = reply_clean.strip()

        result = json.loads(reply_clean)

        results_list.append({
            "event": event,
            "run": j + 1,
            "minp": result["min_prob"],
            "p": result["prob"],
            "maxp": result["max_prob"]
        })


print("Experiment complete.")

# Combine results --------------------------

final_predictions = pd.DataFrame(results_list)
final_predictions["interval_width"] = final_predictions["maxp"] - final_predictions["minp"]
final_predictions["is_interval"] = final_predictions["minp"] != final_predictions["maxp"]

# Display results --------------------------

print(final_predictions)

# Plot results --------------------------

fig, ax = plt.subplots(figsize=(10, 6))

events_reversed = final_predictions["event"].unique()[::-1]
y_positions = {event: i for i, event in enumerate(events_reversed)}

for idx, row in final_predictions.iterrows():
    y_pos = y_positions[row["event"]]
    offset = (row["run"] - 1) * 0.15 - 0.075

    ax.errorbar(
        x=row["p"],
        y=y_pos + offset,
        xerr=[[row["p"] - row["minp"]], [row["maxp"] - row["p"]]],
        fmt='o',
        markersize=8,
        capsize=5
    )

ax.set_yticks(range(len(events_reversed)))
ax.set_yticklabels(events_reversed)
ax.set_xlabel("Probability (%)")
ax.set_title("LLM Probability Predictions with Uncertainty Intervals")
ax.grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.show()

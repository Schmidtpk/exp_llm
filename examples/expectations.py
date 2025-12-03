# expectations.py
# Multiple event probability predictions --------------------------

# Installation:
# pip install openai pandas matplotlib
# (in RStudio using reticulate:
# reticulate::py_install(c("pandas", "matplotlib", "openai"))

import os
import json
import pandas as pd
import matplotlib.pyplot as plt
from openai import OpenAI

# Setup API --------------------------
# os.environ["OPENROUTER_API_KEY"] = "sk-ihr-key-hier"

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)

SYSTEM_PROMPT = "You are an expert forecaster providing probability estimates. Reply with only the requested JSON structure and nothing else."
MODEL = "openai/gpt-oss-120b"

# Define events --------------------------

events = [
    "Trump will be president in 2028",
    "Global average temperature will increase by more than 1.5°C by 2030",
    "AI will pass the Turing test by 2027",
    "Bitcoin price will exceed $100,000 by end of 2026",
    "Humans will land on Mars by 2035"
]

n = 3  # Anzahl der Wiederholungen

# 3. Experiment durchführen --------------------------
results_list = []
print(f"Frage {len(events) * n} Prompts ab...")

for event in events:
    for i in range(n):
        print(f"  ... {event[:15]}... (Run {i+1}/{n})")
        
        prompt = (f"Probability for: '{event}'? Give 0-100%. "
                  'Return valid JSON object with keys: "min_prob", "prob", "max_prob".')

        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                          {"role": "system", "content": SYSTEM_PROMPT},
                          {"role": "user", "content": prompt}
                        ],
                response_format={"type": "json_object"}
            )

            # Robustes Parsing
            content = response.choices[0].message.content
            start = content.find('{')
            end = content.rfind('}') + 1
            
            if start != -1:
                data = json.loads(content[start:end])
                
                results_list.append({
                    "event": event,
                    "run": i,
                    "min": data["min_prob"],
                    "p": data["prob"],
                    "max": data["max_prob"]
                })
        except Exception as e:
            print(f"    Fehler im Run {i+1}: {e}")

# 4. Plotten --------------------------
if results_list:
    df = pd.DataFrame(results_list)
    
    plt.figure(figsize=(10, 6))
    
    # Wir weisen jedem Event eine Nummer auf der Y-Achse zu (0, 1, 2...)
    events_unique = df["event"].unique()
    y_map = {evt: i for i, evt in enumerate(events_unique)}
    
    # Plotten Loop
    for idx, row in df.iterrows():
        base_y = y_map[row["event"]]
        # Kleiner Versatz je nach Run, damit Punkte nicht übereinander liegen
        # Run 0 -> -0.1, Run 1 -> 0.0, Run 2 -> +0.1
        offset = (row["run"] - 1) * 0.1 
        
        plt.errorbar(
            x=row["p"],
            y=base_y + offset,
            xerr=[[row["p"] - row["min"]], [row["max"] - row["p"]]],
            fmt='o',
            color='tab:blue',
            capsize=4
        )

    # Achsenbeschriftung korrigieren
    plt.yticks(range(len(events_unique)), events_unique)
    plt.xlabel("Wahrscheinlichkeit (%)")
    plt.title(f"LLM Vorhersagen ({n} Runs pro Event)")
    plt.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    plt.show()
else:
    print("Keine Ergebnisse.")


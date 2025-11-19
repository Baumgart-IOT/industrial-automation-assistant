import json, yaml
from ollama_local import ask_ollama
from pathlib import Path

with open("config.yaml") as f:
    config = yaml.safe_load(f)
with open("rules_for_llm.json") as f:
    rules = json.load(f)

narratives = {}
for name, info in rules.items():
    prompt = f"""
You are a senior control system engineer with 30 years of experience.
Here are the automatically discovered decision rules that trigger {name} to start:

{info['rules_text']}

Write:
1. One-paragraph plain English control philosophy
2. Pseudo ladder-logic (like Rockwell/PLC style)
3. Detected setpoints and hysteresis
Use clear language suitable for an operator handover document.
"""
    narrative = ask_ollama(prompt)
    narratives[name] = narrative
    print(f"\n=== {name} ===\n{narrative}\n")

Path("control_philosophy.md").write_text("# Control Philosophy\n\n" + 
    "\n\n".join([f"## {name}\n{narratives[name]}" for name in narratives]))
print("Full control philosophy written to control_philosophy.md")

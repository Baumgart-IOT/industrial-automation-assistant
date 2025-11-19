import json
with open("rules.json") as f:
    data = json.load(f)
with open("rules_for_llm.json", "w") as f:
    json.dump(data, f, indent=2)
print("Ready for LLM narration")

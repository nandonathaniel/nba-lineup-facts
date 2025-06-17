import ast
import json

with open("data/2024-25.json", "r", encoding="utf-8") as f:
    raw = f.read()


parsed = ast.literal_eval(raw)


with open("data/2024-25.json", "w", encoding="utf-8") as f:
    json.dump(parsed, f, indent=2)

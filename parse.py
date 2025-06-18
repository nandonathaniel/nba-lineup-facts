import ast
import json

with open("data/new-2020-21.json", "r", encoding="utf-8") as f:
    raw = f.read()


parsed = ast.literal_eval(raw)


with open("data/new-2020-21.json", "w", encoding="utf-8") as f:
    json.dump(parsed, f, indent=2)

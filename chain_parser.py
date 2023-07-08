import json


filename = "chain.json"

with open(filename, "r", encoding="utf-8") as f:
    chain = json.loads(f.read())

for block in chain[1:]:
    block["transactions"] = json.loads(block["transactions"])

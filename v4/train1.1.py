import json

with open("data_full.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("=" * 70)
print("CLINC150 INTENTS")
print("=" * 70)

intents = sorted(set(item[1] for item in data["train"]))

print(f"\nTotal intents: {len(intents)}\n")

for i, intent in enumerate(intents, 1):
    print(f"{i:3}. {intent}")
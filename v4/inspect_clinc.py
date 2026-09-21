import json

with open("data_full.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("=" * 70)
print("CLINC150 DATASET INSPECTION")
print("=" * 70)

# Count rows in each split
for split in ["train", "val", "test", "oos_train", "oos_val", "oos_test"]:
    if split in data:
        print(f"{split:12} : {len(data[split])}")

print("\nSAMPLE DATA")
print("-" * 70)

# Show first 10 samples
for split in ["train", "val", "test"]:
    if split in data:
        print(f"\n{split.upper()}:")

        for item in data[split][:5]:
            print(item)

print("\n" + "=" * 70)
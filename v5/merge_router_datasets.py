import pandas as pd

# Load datasets
original = pd.read_csv("dataset.csv")
clinc = pd.read_csv("clinc_router_data.csv")

# Keep only required columns
original = original[["query", "label"]]
clinc = clinc[["query", "label"]]

# Combine
merged = pd.concat(
    [original, clinc],
    ignore_index=True
)

# Remove any accidental duplicates
merged = merged.drop_duplicates(
    subset=["query", "label"]
)

# Shuffle the dataset
merged = merged.sample(
    frac=1,
    random_state=42
).reset_index(drop=True)

# Save
merged.to_csv(
    "dataset_v5.csv",
    index=False
)

print("=" * 60)
print("MERGED ROUTER DATASET")
print("=" * 60)

print("\nTotal rows:", len(merged))

print("\nClass distribution:")
print(merged["label"].value_counts())

print("\nFirst 10 rows:")
print(merged.head(10).to_string(index=False))

print("\nSaved as: dataset_v5.csv")
print("=" * 60)
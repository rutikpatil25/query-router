import pandas as pd

# Load merged dataset
df = pd.read_csv("dataset_v5.csv")

# Make sure both classes are represented equally
test_local = df[df["label"] == "local"].sample(
    n=500,
    random_state=123
)

test_online = df[df["label"] == "online"].sample(
    n=500,
    random_state=123
)

# Create independent test set
test = pd.concat(
    [test_local, test_online],
    ignore_index=True
)

# Remove test rows from training data
test_indices = test.index

# We need to identify rows using the query itself
test_queries = set(test["query"])

train = df[~df["query"].isin(test_queries)].copy()

# Shuffle both
test = test.sample(
    frac=1,
    random_state=123
).reset_index(drop=True)

train = train.sample(
    frac=1,
    random_state=123
).reset_index(drop=True)

# Save
test.to_csv("independent_test.csv", index=False)
train.to_csv("dataset_v5_train.csv", index=False)

print("=" * 60)
print("INDEPENDENT TEST SET")
print("=" * 60)

print("\nTest rows:", len(test))
print("\nTest distribution:")
print(test["label"].value_counts())

print("\nTraining rows:", len(train))
print("\nTraining distribution:")
print(train["label"].value_counts())

print("\nOverlap check:")
overlap = set(train["query"]) & set(test["query"])
print("Training/Test overlapping queries:", len(overlap))

print("\nSaved:")
print("  dataset_v5_train.csv")
print("  independent_test.csv")

print("=" * 60)
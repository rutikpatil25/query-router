import pandas as pd


original = pd.read_csv("dataset.csv")
clinc = pd.read_csv("clinc_router_data.csv")


# Normalize text for comparison
def normalize(text):
    return " ".join(str(text).lower().strip().split())


original["normalized"] = original["query"].apply(normalize)
clinc["normalized"] = clinc["query"].apply(normalize)


# Exact query overlap
overlap = set(original["normalized"]) & set(clinc["normalized"])


print("=" * 60)
print("DATASET OVERLAP CHECK")
print("=" * 60)

print("\nOriginal dataset rows :", len(original))
print("CLINC dataset rows    :", len(clinc))
print("Exact overlapping queries:", len(overlap))


if overlap:
    print("\nOVERLAPPING QUERIES")
    print("-" * 60)

    for query in sorted(overlap):
        print(query)

else:
    print("\nNo exact query overlap found.")


# Check conflicting labels
print("\n" + "=" * 60)
print("LABEL CONFLICT CHECK")
print("=" * 60)

conflicts = []

for query in overlap:
    original_labels = set(
        original.loc[original["normalized"] == query, "label"]
    )

    clinc_labels = set(
        clinc.loc[clinc["normalized"] == query, "label"]
    )

    if original_labels != clinc_labels:
        conflicts.append(
            (query, original_labels, clinc_labels)
        )


print("Conflicting labels:", len(conflicts))

if conflicts:
    print("\nCONFLICTS:")
    for query, original_labels, clinc_labels in conflicts:
        print(
            f"{query}\n"
            f"  Original: {original_labels}\n"
            f"  CLINC:    {clinc_labels}\n"
        )

print("\n" + "=" * 60)
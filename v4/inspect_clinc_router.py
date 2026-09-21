import pandas as pd

df = pd.read_csv("clinc_router_data.csv")

print("=" * 60)
print("CLINC ROUTER DATA INSPECTION")
print("=" * 60)

for label in ["local", "online"]:
    print("\n" + "-" * 60)
    print(label.upper())
    print("-" * 60)

    sample = df[df["label"] == label].sample(
        n=min(30, len(df[df["label"] == label])),
        random_state=42
    )

    for i, row in enumerate(sample.itertuples(index=False), 1):
        print(f"{i:02}. {row.query}")

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print(df["label"].value_counts())
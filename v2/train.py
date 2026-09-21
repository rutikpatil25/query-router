"""Train and persist the query-routing text classifier."""

from pathlib import Path
import pickle

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


BASE_DIR = Path(__file__).resolve().parent
DATASET_PATH = BASE_DIR / "dataset.csv"
VECTORIZER_PATH = BASE_DIR / "vectorizer.pkl"
MODEL_PATH = BASE_DIR / "trained_model.pkl"


def train() -> None:
    data = pd.read_csv(DATASET_PATH)
    required_columns = {"query", "label"}
    if not required_columns.issubset(data.columns):
        raise ValueError("dataset.csv must contain 'query' and 'label' columns")
    if data.empty:
        raise ValueError("dataset.csv must contain at least one training row")

    vectorizer = TfidfVectorizer(lowercase=True, ngram_range=(1, 2), sublinear_tf=True)
    model = LogisticRegression(max_iter=1000, random_state=42)
    features = vectorizer.fit_transform(data["query"].astype(str))
    model.fit(features, data["label"].astype(str))

    with VECTORIZER_PATH.open("wb") as file:
        pickle.dump(vectorizer, file)
    with MODEL_PATH.open("wb") as file:
        pickle.dump(model, file)

    print("Saved vectorizer to", VECTORIZER_PATH)
    print("Saved model to", MODEL_PATH)


if __name__ == "__main__":
    train()

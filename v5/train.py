"""Train and persist the query-routing text classifier."""

from pathlib import Path
import pickle

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split


BASE_DIR = Path(__file__).resolve().parent
DATASET_PATH = BASE_DIR / "dataset_v5.csv"
VECTORIZER_PATH = BASE_DIR / "vectorizer.pkl"
MODEL_PATH = BASE_DIR / "trained_model.pkl"


def train() -> None:
    if not DATASET_PATH.is_file():
        print(f"ERROR: Dataset file not found: {DATASET_PATH}")
        print("Place the configured dataset file in the v4 folder and try again.")
        raise SystemExit(1)

    # 1.Extract (Gathering the Raw Data)
    # loading = dataset
    data = pd.read_csv(DATASET_PATH)
    required_columns = {"query", "label"}
    if not required_columns.issubset(data.columns):
        raise ValueError("dataset.csv must contain 'query' and 'label' columns")
    if data.empty:
        raise ValueError("dataset.csv must contain at least one training row")
    
    queries = data["query"].astype(str)
    labels = data["label"].astype(str)

    # 2.Transform (Preparing the Data for the Model)
    train_queries, validation_queries, train_labels, validation_labels = (
        train_test_split(
            queries,
            labels,
            test_size=0.2,
            random_state=42,
            stratify=labels,
        )
    )

    # preparing the text vectorizer
    vectorizer = TfidfVectorizer(
        lowercase=True, ngram_range=(1, 2), sublinear_tf=True # 1 and 2 for unigrams and biagrams (single words and pair of words)
    )
    train_features = vectorizer.fit_transform(train_queries)
    validation_features = vectorizer.transform(validation_queries)
    model = LogisticRegression(C=0.01, max_iter=1000, random_state=42)
    model.fit(train_features, train_labels)


    predictions = model.predict(validation_features)
    label_order = ["local", "online"]
    print("\nValidation Metrics (20% unseen holdout)")
    print("---------------------------------------")
    print(f"Validation rows: {len(validation_labels)}")
    print(f"Accuracy:  {accuracy_score(validation_labels, predictions):.4f}")
    print(
        "Precision: "
        f"{precision_score(validation_labels, predictions, average='weighted', zero_division=0):.4f}"
    )
    print(
        "Recall:    "
        f"{recall_score(validation_labels, predictions, average='weighted', zero_division=0):.4f}"
    )
    print("\nClassification Report (validation set)")
    print(
        classification_report(
            validation_labels,
            predictions,
            labels=label_order,
            zero_division=0,
        )
    )
    print("Confusion Matrix (validation set)")
    print("---------------------------------")
    print(f"Labels: {label_order}")
    print(confusion_matrix(validation_labels, predictions, labels=label_order))

    # 3.Load (Saving the Processed Assets)
    with VECTORIZER_PATH.open("wb") as file:
        pickle.dump(vectorizer, file)
    with MODEL_PATH.open("wb") as file:
        pickle.dump(model, file)

    print("Saved vectorizer to", VECTORIZER_PATH)
    print("Saved model to", MODEL_PATH)


if __name__ == "__main__":
    train()

import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)

import pickle


print("=" * 60)
print("             TRAINING MODEL")
print("=" * 60)


# ============================================================
# 1. LOAD TRAINING DATA
# ============================================================

df = pd.read_csv("dataset_v5_train.csv")

X = df["query"]
y = df["label"]

print("\nTraining dataset")
print("----------------")
print("Rows:", len(df))
print("Local:", (y == "local").sum())
print("Online:", (y == "online").sum())


# ============================================================
# 2. TRAIN / VALIDATION SPLIT
# ============================================================

X_train, X_val, y_train, y_val = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# ============================================================
# 3. TF-IDF
# ============================================================

vectorizer = TfidfVectorizer(
    lowercase=True,
    ngram_range=(1, 2),
    sublinear_tf=True
)

X_train_tfidf = vectorizer.fit_transform(X_train)
X_val_tfidf = vectorizer.transform(X_val)


# ============================================================
# 4. LOGISTIC REGRESSION
# ============================================================

model = LogisticRegression(
    C=0.01,
    max_iter=1000,
    random_state=42
)

model.fit(X_train_tfidf, y_train)


# ============================================================
# 5. VALIDATION EVALUATION
# ============================================================

val_predictions = model.predict(X_val_tfidf)

val_accuracy = accuracy_score(y_val, val_predictions)
val_precision = precision_score(
    y_val,
    val_predictions,
    average="weighted"
)
val_recall = recall_score(
    y_val,
    val_predictions,
    average="weighted"
)
val_f1 = f1_score(
    y_val,
    val_predictions,
    average="weighted"
)

print("\n" + "=" * 60)
print("VALIDATION RESULTS")
print("=" * 60)

print("\nValidation rows:", len(y_val))
print(f"Accuracy:  {val_accuracy:.4f}")
print(f"Precision: {val_precision:.4f}")
print(f"Recall:    {val_recall:.4f}")
print(f"F1 Score:  {val_f1:.4f}")

print("\nClassification Report")
print("-" * 60)
print(classification_report(y_val, val_predictions))

print("Confusion Matrix")
print("-" * 60)
print("Labels:", model.classes_)
print(confusion_matrix(y_val, val_predictions))


# ============================================================
# 6. INDEPENDENT TEST SET
# ============================================================

test_df = pd.read_csv("independent_test.csv")

X_test = test_df["query"]
y_test = test_df["label"]

X_test_tfidf = vectorizer.transform(X_test)

test_predictions = model.predict(X_test_tfidf)


# ============================================================
# 7. INDEPENDENT TEST EVALUATION
# ============================================================

test_accuracy = accuracy_score(y_test, test_predictions)
test_precision = precision_score(
    y_test,
    test_predictions,
    average="weighted"
)
test_recall = recall_score(
    y_test,
    test_predictions,
    average="weighted"
)
test_f1 = f1_score(
    y_test,
    test_predictions,
    average="weighted"
)

print("\n" + "=" * 60)
print("INDEPENDENT TEST RESULTS")
print("=" * 60)

print("\nTest rows:", len(y_test))
print(f"Accuracy:  {test_accuracy:.4f}")
print(f"Precision: {test_precision:.4f}")
print(f"Recall:    {test_recall:.4f}")
print(f"F1 Score:  {test_f1:.4f}")

print("\nClassification Report")
print("-" * 60)
print(classification_report(y_test, test_predictions))

print("Confusion Matrix")
print("-" * 60)
print("Labels:", model.classes_)
print(confusion_matrix(y_test, test_predictions))


# ============================================================
# 8. SAVE MODEL
# ============================================================

with open("vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

with open("trained_model.pkl", "wb") as f:
    pickle.dump(model, f)


# ============================================================
# 9. FINAL SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("MODEL SAVED")
print("=" * 60)

print("vectorizer.pkl")
print("trained_model.pkl")

print("\nFinal comparison")
print("-" * 60)
print(f"Validation accuracy:       {val_accuracy:.4f}")
print(f"Independent test accuracy: {test_accuracy:.4f}")

print("=" * 60)
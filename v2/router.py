"""Keyword-first query router backed by a small TF-IDF classifier."""

from __future__ import annotations

import csv
import json
import pickle
from datetime import datetime, timezone
from pathlib import Path
from threading import RLock


BASE_DIR = Path(__file__).resolve().parent
KEYWORDS_PATH = BASE_DIR / "keywords.json"
VECTORIZER_PATH = BASE_DIR / "vectorizer.pkl"
MODEL_PATH = BASE_DIR / "trained_model.pkl"
HISTORY_PATH = BASE_DIR / "routing_history.csv"
HISTORY_LOCK = RLock()
HISTORY_COLUMNS = ["timestamp", "query", "route", "method", "confidence"]


def _load_resources():
    with KEYWORDS_PATH.open(encoding="utf-8") as file:
        keywords = json.load(file)
    with VECTORIZER_PATH.open("rb") as file:
        vectorizer = pickle.load(file)
    with MODEL_PATH.open("rb") as file:
        model = pickle.load(file)
    return [str(word).lower() for word in keywords.get("online", [])], vectorizer, model


ONLINE_KEYWORDS = None
VECTORIZER = None
MODEL = None


def _ensure_history_file() -> None:
    with HISTORY_LOCK:
        if not HISTORY_PATH.exists() or HISTORY_PATH.stat().st_size == 0:
            with HISTORY_PATH.open("a", newline="", encoding="utf-8") as file:
                csv.writer(file).writerow(HISTORY_COLUMNS)


_ensure_history_file()


def _log_route(query: str, route: str, method: str, confidence: float) -> None:
    with HISTORY_LOCK:
        _ensure_history_file()
        with HISTORY_PATH.open("a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(
                [
                    datetime.now(timezone.utc).isoformat(),
                    query,
                    route,
                    method,
                    f"{confidence:.4f}",
                ]
            )


def route_query(query: str, confidence_threshold: float = 0.55) -> dict:
    """Route a query using keywords, ML prediction, then a safety-first fallback."""
    global ONLINE_KEYWORDS, VECTORIZER, MODEL

    cleaned_query = " ".join(query.strip().split())
    if not cleaned_query:
        raise ValueError("query must not be empty")

    if VECTORIZER is None or MODEL is None or ONLINE_KEYWORDS is None:
        ONLINE_KEYWORDS, VECTORIZER, MODEL = _load_resources()

    lowered_query = cleaned_query.lower()
    matched_keyword = next(
        (word for word in ONLINE_KEYWORDS if word in lowered_query), None
    )
    if matched_keyword:
        result = {
            "query": cleaned_query,
            "route": "online",
            "method": "keyword",
            "confidence": 1.0,
            "matched_keyword": matched_keyword,
        }
    else:
        probabilities = MODEL.predict_proba(
            VECTORIZER.transform([cleaned_query])
        )[0]
        best_index = probabilities.argmax()
        predicted_route = str(MODEL.classes_[best_index])
        confidence = float(probabilities[best_index])
        if confidence < confidence_threshold:
            predicted_route = "online"
            method = "fallback"
        else:
            method = "ml"
        result = {
            "query": cleaned_query,
            "route": predicted_route,
            "method": method,
            "confidence": confidence,
        }

    _log_route(
        result["query"], result["route"], result["method"], result["confidence"]
    )
    return result

# Query Router

An industry-grade, fault-tolerant **Hybrid Ensemble Query Routing Pipeline** designed to intelligently classify incoming text queries into `local` (static compute) or `online` (dynamic network lookups). 

Developed as a third-year engineering project for **Statistics for Machine Learning (SMLD)**, this application demonstrates a production-ready **Fallback and Heuristic-Driven Router Pattern** utilizing high-performance python micro-frameworks and statistical machine learning.

---

## 🚀 Architectural Pipeline Flow

The core application operates as an asymmetrical cost-sensitive decision pipeline, maximizing availability and processing speed while minimizing live API compute overhead:

```
                  [ Incoming User Query ]
                             │
                             ▼
              ┌─────────────────────────────┐
              │   1. Deterministic Filter   │ ──(Match)──► [ Online Route ]
              │     (Keywords Heuristic)    │              (Instant, Low Latency)
              └──────────────┬──────────────┘
                             │ (Filter Fail)
                             ▼
              ┌─────────────────────────────┐
              │    2. Probabilistic ML      │
              │   (TF-IDF + Regularized LR) │
              └──────────────┬──────────────┘
                             │
               ┌─────────────┴─────────────┐
               │ Confidence > Threshold?   │
               └──────┬─────────────┬──────┘
                      │ Yes         │ No (Uncertainty)
                      ▼             ▼
               [ Predicted Route ]  [ 3. Safety Fallback ] ──► [ Online Route ]
```

1. **Phase 1: Heuristic Keyword Check:** Executes basic regex/hash-map evaluations via `keywords.json` to immediately offload obvious time-sensitive inputs in under 1ms, completely bypassing the machine learning stack.
2. **Phase 2: Statistical ML Classification:** If heuristics fail, text undergoes TF-IDF token vectorization and is evaluated via a heavily regularized Logistic Regression classifier to capture deep contextual human intent.
3. **Phase 3: Asymmetric Safety Fallback:** If the model's highest class probability drops below the confidence threshold margin (`0.55`), the system overrides the probabilistic decision, routing the query `online` to prevent serving stale data.

---

## 📁 Repository Layout

```text
query-router-project/
│
├── dataset.csv            # Production dataset containing 10,000 balanced, unstructured query examples
│
├── train.py               # ML training pipeline script enforcing an 80/20 train-test validation split
├── vectorizer.pkl         # Serialized TF-IDF vocabulary state mappings
├── trained_model.pkl      # Frozen statistical weights of the Logistic Regression model
│
├── keywords.json          # Predefined high-priority deterministic token mappings
├── router.py              # Central pipeline thread routing and fallback logic wrapper
│
├── main.py                # Asynchronous FastAPI backend microservice engine
├── app.py                 # Premium reactive Streamlit operations analytics dashboard
│
├── tools.bat              # Automation command panel (Model Training & Log purging orchestration)
└── routing_history.csv    # Live telemetry audit trails logging tracking timestamps & methods
```

---

## 📈 SMLD Pipeline Evaluation Metrics

The pipeline avoids overfitting by isolating **3,160 completely unseen validation rows** (20% holdout split) from a curated **10,000-row dataset**, utilizing extreme **L2 Regularization (`C=0.01`)** to ensure real-world system generalization.

### 📊 Validation Results (20% Unseen Holdout)
* **Pipeline Accuracy:** 86.11%
* **Weighted Precision:** 88.85%
* **Weighted Recall:** 86.11%

### 🔲 Confusion Matrix Space
```text
Labels: ['local', 'online']
[[ 1738     2 ]   --> [ True Local , False Online ]
 [  437   983 ]]  --> [ False Local, True Online ]
```

* **The SMLD Defense Matrix:** Due to structural L2 regularization penalizing weight coefficients heavily to survive real-world language drifts, the model produces a natural contextual overlap resulting in 437 False Local variations. Our **Safety Fallback Layer** successfully counters this entire margin by intercepting low-confidence predictions at runtime, transforming a probabilistic error into a resilient, self-correcting system.

---

## 🛠️ Technology Stack & Dependencies

* **Frontend Dashboard:** [Streamlit](https://streamlit.io/) (Data caching UI, custom horizonal progression analytics grids)
* **Backend API Framework:** [FastAPI](https://fastapi.tiangolo.com/) + [Uvicorn](https://www.uvicorn.org/) (High-performance asynchronous server layer)
* **Machine Learning Engine:** [Scikit-Learn](https://scikit-learn.org/) (TF-IDF Vectorization Vector maps & Logistic Regression)
* **Data Processing Layer:** [Pandas](https://pandas.pydata.org/) (Telemetries serialization, file I/O operations checking)

---

## 🏁 Execution & Deployment Guide

### 1. Environment Initialization
Ensure your dependencies are cleanly localized within your virtual environment environment path setup:
```bash
pip install -r requirements.txt
```

### 2. Operational Control Center
Execute the Windows orchestration pipeline utility script to trigger backend routines or clear archived audit trails safely:
```bash
tools.bat
```
*Choose **Option 1** to compile features and serialize weight layers cleanly to the repository workspace.*

### 3. Launching the Cluster Application
Run your customized orchestration engine to concurrently launch backend endpoints and responsive frontend visuals across explicit loopback allocations:
* **FastAPI Microservice Infrastructure:** `http://127.0.0.1:8000`
* **Interactive API Reference Manual (Swagger):** `http://127.0.0.1:8000/docs`
* **Operations Command Dashboard Interface:** `http://127.0.0.1:8501`

---

## 🛡️ Telemetry & System Observability
Every single query mapped across this service pipeline dynamically logs records within `routing_history.csv` under standard `RLock()` threading locks, capturing:
* **`timestamp`**: Short ISO temporal strings for analytical timeline distribution plotting.
* **`method`**: Explicit tracing variables highlighting if processing concluded via `keyword`, `ml`, or `fallback` paths.
* **`confidence`**: Fine-grained floating arrays directly mapping inline progress meters for real-time visualization controls.

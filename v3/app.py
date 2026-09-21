"""Streamlit dashboard for the query router."""

import csv

import pandas as pd
import streamlit as st

from router import HISTORY_PATH, route_query


st.set_page_config(page_title="Query Router", page_icon="🔀", layout="wide")
st.title("Query Router")


def load_history() -> pd.DataFrame:
    """Load routing history once per Streamlit run."""
    if not HISTORY_PATH.exists() or HISTORY_PATH.stat().st_size == 0:
        return pd.DataFrame()

    with HISTORY_PATH.open(newline="", encoding="utf-8") as file:
        history = pd.DataFrame(list(csv.DictReader(file)))

    if history.empty:
        return history

    history["timestamp"] = pd.to_datetime(history["timestamp"], errors="coerce")
    history["confidence"] = pd.to_numeric(
        history["confidence"], errors="coerce"
    ).clip(0.0, 1.0)
    return history


def render_history(history: pd.DataFrame) -> None:
    """Render history metrics, logs, and breakdown charts."""
    online_requests = int(history["route"].eq("online").sum())
    local_requests = int(history["route"].eq("local").sum())

    metric_columns = st.columns(3)
    metric_columns[0].metric("Total Pipeline Vol", len(history))
    metric_columns[1].metric("Online Requests", online_requests)
    metric_columns[2].metric("Local Requests", local_requests)

    st.dataframe(
        history.tail(20),
        use_container_width=True,
        hide_index=True,
        column_config={
            "timestamp": st.column_config.DatetimeColumn(
                "Timestamp", format="MMM D, YYYY · h:mm A"
            ),
            "query": st.column_config.TextColumn("Query", width="large"),
            "route": st.column_config.SelectboxColumn(
                "Route", options=["local", "online"], required=True
            ),
            "method": st.column_config.TextColumn("Method"),
            "confidence": st.column_config.ProgressColumn(
                "Confidence", min_value=0.0, max_value=1.0, format="%.2f"
            ),
        },
    )

    chart_columns = st.columns(2)
    with chart_columns[0]:
        st.caption("Route distribution")
        st.bar_chart(history["route"].value_counts(), color="#4F46E5")
    with chart_columns[1]:
        st.caption("Processing method breakdown")
        st.bar_chart(history["method"].value_counts(), color="#0EA5E9")


query = st.text_input(
    "Query",
    placeholder="Find a coffee shop near me",
    label_visibility="collapsed",
)
if st.button("Route query", type="primary"):
    if not query.strip():
        st.warning("Please enter a query.")
    else:
        try:
            result = route_query(query)
            with st.container(border=True):
                st.success(f"Query routed {result['route']}")
                st.json(result)
        except FileNotFoundError:
            st.error("Model files are missing. Run `python train.py` first.")
        except ValueError as error:
            st.error(str(error))

st.divider()
st.subheader("Routing history")
history = load_history()
if not history.empty:
    render_history(history)
else:
    empty_metrics = st.columns(3)
    empty_metrics[0].metric("Total Pipeline Vol", 0)
    empty_metrics[1].metric("Online Requests", 0)
    empty_metrics[2].metric("Local Requests", 0)
    st.info("No queries have been routed yet.")

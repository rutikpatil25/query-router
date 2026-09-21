"""Streamlit dashboard for the query router."""

import csv
from pathlib import Path

import pandas as pd
import streamlit as st

from router import HISTORY_PATH, route_query


st.set_page_config(page_title="Query Router", page_icon="🔀")
st.title("Local / Online Query Router")
st.caption("Keyword check → ML model → safety-first online fallback")

query = st.text_input("Enter a query", placeholder="Find a coffee shop near me")
if st.button("Route query", type="primary"):
    if not query.strip():
        st.warning("Please enter a query.")
    else:
        try:
            result = route_query(query)
            st.success(f"Route: {result['route']}")
            st.json(result)
        except FileNotFoundError:
            st.error("Model files are missing. Run `python train.py` first.")
        except ValueError as error:
            st.error(str(error))

st.divider()
st.subheader("Routing history")
history = pd.DataFrame()
if HISTORY_PATH.exists() and HISTORY_PATH.stat().st_size > 0:
    with HISTORY_PATH.open(newline="", encoding="utf-8") as file:
        history = pd.DataFrame(list(csv.DictReader(file)))

if not history.empty:
    st.dataframe(history.tail(20), use_container_width=True)
    counts = history["route"].value_counts()
    st.metric("Total queries", len(history))
    st.bar_chart(counts)
else:
    st.info("No queries have been routed yet.")

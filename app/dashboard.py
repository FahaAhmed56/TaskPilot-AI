import json
import pandas as pd
import streamlit as st
from taskpilot.core import rank_tasks

st.set_page_config(page_title="TaskPilot AI", page_icon="🎯", layout="wide")
st.title("🎯 TaskPilot AI — Explainable Task Prioritization")
st.caption("Rule-based intelligent scoring demo; not a trained machine-learning model.")
example = pd.read_csv("data/sample_tasks.csv")
upload = st.file_uploader("Upload tasks CSV (title, description, impact, effort, due_date)", type=["csv"])
frame = pd.read_csv(upload) if upload else example
st.dataframe(frame, use_container_width=True)
if st.button("Prioritize tasks", type="primary"):
    try:
        tasks = frame.fillna("").to_dict(orient="records")
        ranked = rank_tasks(tasks)
        output = pd.DataFrame([{**item, "reasons": "; ".join(item["reasons"])} for item in ranked])
        a,b,c = st.columns(3)
        a.metric("Tasks", len(output))
        b.metric("Critical", sum(output.priority == "Critical"))
        c.metric("High", sum(output.priority == "High"))
        st.dataframe(output, use_container_width=True)
        st.bar_chart(output.set_index("title")["score"])
        st.download_button("Download ranked CSV", output.to_csv(index=False), "ranked_tasks.csv", "text/csv")
        st.download_button("Download JSON", json.dumps(ranked, indent=2, default=str), "ranked_tasks.json", "application/json")
    except (ValueError, TypeError) as exc:
        st.error(f"Invalid input: {exc}")

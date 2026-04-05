"""Financial Report Generator — Streamlit Web UI."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import streamlit as st
import pandas as pd

from src.financial_reporter.core import (
    load_config,
    compute_financial_metrics,
    compute_ratios,
    compare_periods,
    forecast_metrics,
    generate_executive_summary,
    generate_financial_report,
    generate_cash_flow_narrative,
    check_ollama_running,
)

# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------
st.set_page_config(page_title="💰 Financial Report Generator", layout="wide", page_icon="💰")

config = load_config(os.getenv("CONFIG_PATH", "config.yaml"))

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
st.sidebar.title("💰 Financial Reporter")
uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])
period = st.sidebar.text_input("Reporting Period", value="Q4-2024")
report_type = st.sidebar.radio("Report Type", ["Full Report", "Executive Summary"])

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _load_data_from_upload(upload) -> tuple[pd.DataFrame, list[dict]]:
    """Return both a DataFrame (for display) and list-of-dicts (for core)."""
    df = pd.read_csv(upload)
    rows = df.to_dict(orient="records")
    return df, rows

# ---------------------------------------------------------------------------
# Tabs
# ---------------------------------------------------------------------------

tab_upload, tab_report, tab_ratios, tab_comparison = st.tabs(
    ["📂 Data Upload", "📝 Report Sections", "📊 Ratio Cards", "📈 Period Comparison"]
)

# ---- Tab 1: Data Upload --------------------------------------------------
with tab_upload:
    st.header("📂 Data Upload & Preview")
    if uploaded_file is not None:
        df, data_rows = _load_data_from_upload(uploaded_file)
        st.success(f"Loaded {len(df)} rows × {len(df.columns)} columns")
        st.dataframe(df, use_container_width=True)

        # Store in session state for other tabs
        st.session_state["df"] = df
        st.session_state["data_rows"] = data_rows
        st.session_state["metrics"] = compute_financial_metrics(data_rows)
    else:
        st.info("Upload a CSV file in the sidebar to get started.")

# ---- Tab 2: Report Sections -----------------------------------------------
with tab_report:
    st.header("📝 Report Sections")
    if "data_rows" not in st.session_state:
        st.warning("Upload data first.")
    else:
        data_rows = st.session_state["data_rows"]
        metrics = st.session_state["metrics"]

        ollama_ok = check_ollama_running()
        if not ollama_ok:
            st.error("Ollama is not running. Start it with `ollama serve`.")
        else:
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("Generate Executive Summary"):
                    with st.spinner("Generating..."):
                        text = generate_executive_summary(metrics, period)
                    st.markdown(text)
            with col2:
                if st.button("Generate Income Analysis"):
                    with st.spinner("Generating..."):
                        text = generate_financial_report(data_rows, metrics, period)
                    st.markdown(text)
            with col3:
                if st.button("Generate Cash Flow Analysis"):
                    with st.spinner("Generating..."):
                        text = generate_cash_flow_narrative(data_rows, metrics)
                    st.markdown(text)

# ---- Tab 3: Ratio Cards ---------------------------------------------------
with tab_ratios:
    st.header("📊 Financial Ratio Cards")
    if "metrics" not in st.session_state:
        st.warning("Upload data first.")
    else:
        metrics = st.session_state["metrics"]
        ratios = compute_ratios(metrics)

        cols = st.columns(len(ratios) if ratios else 1)
        for idx, (name, value) in enumerate(ratios.items()):
            with cols[idx % len(cols)]:
                label = name.replace("_", " ").title()
                st.metric(label=label, value=f"{value:.2%}")

        if not ratios:
            st.info("Not enough data to compute ratios. Ensure 'revenue', 'expenses', and 'net_income' columns exist.")

# ---- Tab 4: Period Comparison Charts ----------------------------------------
with tab_comparison:
    st.header("📈 Period Comparison")
    if "df" not in st.session_state:
        st.warning("Upload data first.")
    else:
        df = st.session_state["df"]
        data_rows = st.session_state["data_rows"]

        # Detect a period/label column (first non-numeric column)
        label_col = None
        for c in df.columns:
            if df[c].dtype == object:
                label_col = c
                break

        if label_col and len(df[label_col].unique()) >= 2:
            periods_available = df[label_col].unique().tolist()
            c1, c2 = st.columns(2)
            with c1:
                current = st.selectbox("Current Period", periods_available, index=len(periods_available) - 1)
            with c2:
                previous = st.selectbox("Previous Period", periods_available, index=0)

            comparison = compare_periods(data_rows, current, previous)

            # Bar chart of changes
            if comparison["changes"]:
                change_df = pd.DataFrame(
                    {
                        "Metric": list(comparison["changes"].keys()),
                        "Change (%)": [v["percentage"] for v in comparison["changes"].values()],
                    }
                )
                st.subheader("Change (%)")
                st.bar_chart(change_df.set_index("Metric"))

            # Trend line of numeric columns
            numeric_cols = df.select_dtypes(include="number").columns.tolist()
            if numeric_cols:
                st.subheader("Trend Lines")
                st.line_chart(df[numeric_cols])
        else:
            # Fall back to simple trend lines
            numeric_cols = df.select_dtypes(include="number").columns.tolist()
            if numeric_cols:
                st.subheader("Trend Lines")
                st.line_chart(df[numeric_cols])
            else:
                st.info("No numeric columns found for charting.")

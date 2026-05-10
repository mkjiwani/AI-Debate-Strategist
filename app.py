"""AI Debate Strategist — Multi-Layer Reasoning App.

A Streamlit application that implements a 5-layer AI reasoning system
for analyzing cricket debate topics, with full telemetry tracking.

Usage:
    streamlit run app.py
"""

import os
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

from prompts import TOPICS
from reasoning import run_debate_analysis
from telemetry import TelemetryTracker

# Load environment variables from .env file
load_dotenv()


# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="AI Debate Strategist",
    page_icon="🏏",
    layout="wide",
)

# ---------------------------------------------------------------------------
# Sidebar — configuration
# ---------------------------------------------------------------------------
st.sidebar.title("⚙️ Configuration")

env_api_key = os.getenv("OPENAI_API_KEY", "")
api_key = st.sidebar.text_input(
    "OpenAI API Key",
    value=env_api_key,
    type="password",
    help="Loaded from .env if set. You can override it here.",
)

default_model = os.getenv("DEFAULT_MODEL", "gpt-4o-mini")
model_options = ["gpt-4o-mini", "gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"]
model = st.sidebar.selectbox(
    "Model",
    model_options,
    index=model_options.index(default_model) if default_model in model_options else 0,
    help="Select the model. gpt-4o-mini is cost-effective; gpt-4o provides deeper reasoning.",
)

topic = st.sidebar.selectbox("Debate Topic", TOPICS)

st.sidebar.markdown("---")
st.sidebar.markdown(
    "**How it works:** The app runs 5 sequential reasoning layers, "
    "each building on the previous layer's output. Telemetry is "
    "captured for every API call."
)

# ---------------------------------------------------------------------------
# Main UI
# ---------------------------------------------------------------------------
st.title("🏏 AI Debate Strategist")
st.markdown(
    "A **multi-layer AI reasoning system** that analyzes cricket debate topics "
    "through 5 progressive layers — from context analysis to final strategic position."
)

# Layer descriptions for reference
with st.expander("📋 Reasoning Layers Overview", expanded=False):
    st.markdown("""
| Layer | Purpose | Guiding Question |
|-------|---------|-----------------|
| **1. Context Analysis** | Understand the problem, define the question, identify key factors | *What is the problem and what influences it?* |
| **2. Argument Builder** | Take a clear position with structured logic | *What is my position and why?* |
| **3. Counter Argument** | Generate the strongest opposing viewpoint | *What is the strongest opposing view?* |
| **4. Self-Critique** | Identify weaknesses, gaps, or bias | *Where is my argument weak?* |
| **5. Final Strategy** | Synthesize into a balanced, informed conclusion | *What is the most informed answer?* |
""")

# ---------------------------------------------------------------------------
# Run analysis
# ---------------------------------------------------------------------------
run_btn = st.button("🚀 Run Debate Analysis", type="primary", use_container_width=True)

if run_btn:
    if not api_key:
        st.error("Please enter your OpenAI API key in the sidebar.")
        st.stop()
    client = OpenAI(api_key=api_key)

    tracker = TelemetryTracker()

    # Progress tracking
    progress_bar = st.progress(0, text="Initializing...")
    status_area = st.empty()

    def on_progress(layer_name, layer_num):
        progress_bar.progress(
            (layer_num - 1) / 5,
            text=f"Running {layer_name} ({layer_num}/5)...",
        )
        status_area.info(f"⏳ Processing **{layer_name}**...")

    try:
        results = run_debate_analysis(client, model, topic, tracker, on_progress)
        progress_bar.progress(1.0, text="✅ Analysis complete!")
        status_area.success("All 5 reasoning layers completed successfully.")

        # Store results in session state
        st.session_state["results"] = results
        st.session_state["tracker"] = tracker
        st.session_state["topic"] = topic
        st.session_state["model"] = model

    except Exception as e:
        progress_bar.empty()
        status_area.error(f"Error: {e}")
        st.stop()

# ---------------------------------------------------------------------------
# Display results
# ---------------------------------------------------------------------------
if "results" in st.session_state:
    results = st.session_state["results"]
    tracker = st.session_state["tracker"]

    st.markdown("---")
    st.header("📊 Reasoning Results")
    st.caption(f"Topic: {st.session_state['topic']}  |  Model: {st.session_state['model']}")

    # Tabbed display for each layer
    layer_names = list(results.keys())
    tabs = st.tabs(layer_names)

    for tab, layer_name in zip(tabs, layer_names):
        with tab:
            st.markdown(results[layer_name])

    # -----------------------------------------------------------------------
    # Telemetry dashboard
    # -----------------------------------------------------------------------
    st.markdown("---")
    st.header("📈 AI Telemetry Dashboard")

    # Summary metrics row
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Input Tokens", f"{tracker.total_input_tokens:,}")
    col2.metric("Total Output Tokens", f"{tracker.total_output_tokens:,}")
    col3.metric("Total Tokens", f"{tracker.total_tokens:,}")
    col4.metric("Total Latency", f"{tracker.total_latency_ms:,.0f}ms")

    # Per-layer breakdown table
    st.subheader("Per-Layer Breakdown")
    telemetry_data = []
    for m in tracker.layers:
        telemetry_data.append({
            "Layer": m.layer_name,
            "Input Tokens": m.input_tokens,
            "Output Tokens": m.output_tokens,
            "Total Tokens": m.total_tokens,
            "Latency (ms)": round(m.latency_ms),
            "Tokens/sec": round(m.tokens_per_second, 1),
        })

    df = pd.DataFrame(telemetry_data)
    st.dataframe(df, use_container_width=True, hide_index=True)

    # Charts
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.subheader("Token Usage by Layer")
        chart_df = df[["Layer", "Input Tokens", "Output Tokens"]].set_index("Layer")
        st.bar_chart(chart_df)

    with chart_col2:
        st.subheader("Latency by Layer (ms)")
        latency_df = df[["Layer", "Latency (ms)"]].set_index("Layer")
        st.bar_chart(latency_df)

    # Optimization insights
    st.subheader("🔍 Optimization Insights")
    insights = tracker.get_optimization_insights()
    for insight in insights:
        st.markdown(f"- {insight}")

    # Token efficiency summary
    st.markdown("---")
    st.subheader("📋 Telemetry Summary")
    summary_col1, summary_col2 = st.columns(2)
    with summary_col1:
        st.markdown(f"""
        | Metric | Value |
        |--------|-------|
        | **Total Input Tokens** | {tracker.total_input_tokens:,} |
        | **Total Output Tokens** | {tracker.total_output_tokens:,} |
        | **Total Tokens** | {tracker.total_tokens:,} |
        | **Total Latency** | {tracker.total_latency_ms:,.0f}ms |
        | **Avg Latency/Layer** | {tracker.avg_latency_ms:,.0f}ms |
        | **Avg Throughput** | {tracker.avg_tokens_per_second:,.1f} tokens/sec |
        """)
    with summary_col2:
        st.markdown(f"""
        **Model:** {st.session_state['model']}

        **Layers executed:** {len(tracker.layers)}

        **Input/Output ratio:** {
            (tracker.total_output_tokens / tracker.total_input_tokens * 100)
            if tracker.total_input_tokens > 0 else 0
        :.1f}% — output tokens as percentage of input tokens.
        """)

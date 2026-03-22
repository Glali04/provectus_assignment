import streamlit as st
import plotly.express as px

from utils.load_from_db import load_usage_data
from utils.filters import apply_filters

st.set_page_config(layout="wide")
st.title("🏠 Claude Usage Analytics Dashboard")
st.markdown("A dashboard for analyzing Claude Code API usage, cost, performance, and developer activity.")

df = load_usage_data()

if df.empty:
    st.warning("No data found in the database.")
    st.stop()

df = apply_filters(df)

if df.empty:
    st.warning("No data matches the selected filters.")
    st.stop()

# KPIs
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Tokens", f"{int(df['total_tokens'].sum()):,}")
col2.metric("Total Cost ($)", f"{df['cost_usd'].sum():.2f}")
col3.metric("Active Users", int(df["email"].nunique()))
col4.metric("Sessions", int(df["session_id"].nunique()))

st.markdown("---")

# Key insights
st.subheader("🧠 Key Insights")

top_model = (
    df.groupby("model")["total_tokens"]
    .sum()
    .sort_values(ascending=False)
    .index[0]
)

top_practice = (
    df.groupby("practice")["total_tokens"]
    .sum()
    .sort_values(ascending=False)
    .index[0]
)

peak_hour = (
    df.groupby("hour")["total_tokens"]
    .sum()
    .sort_values(ascending=False)
    .index[0]
)

insight_col1, insight_col2, insight_col3 = st.columns(3)

insight_col1.info(f"**Top model:** {top_model}")
insight_col2.info(f"**Top practice:** {top_practice}")
insight_col3.info(f"**Peak usage hour:** {int(peak_hour)}:00")

st.markdown("---")

# Main charts
left_col, right_col = st.columns(2)

with left_col:
    st.subheader("Token Usage Over Time")

    trend = (
        df.groupby("date")["total_tokens"]
        .sum()
        .reset_index()
    )

    fig_trend = px.line(trend, x="date", y="total_tokens")
    st.plotly_chart(fig_trend, use_container_width=True)

with right_col:
    st.subheader("Cost Over Time")

    cost_trend = (
        df.groupby("date")["cost_usd"]
        .sum()
        .reset_index()
    )

    fig_cost = px.line(cost_trend, x="date", y="cost_usd")
    st.plotly_chart(fig_cost, use_container_width=True)

st.markdown("---")

# Quick breakdowns
bottom_left, bottom_right = st.columns(2)

with bottom_left:
    st.subheader("Usage by Practice")

    practice_data = (
        df.groupby("practice")["total_tokens"]
        .sum()
        .reset_index()
        .sort_values(by="total_tokens", ascending=False)
    )

    fig_practice = px.bar(practice_data, x="practice", y="total_tokens")
    st.plotly_chart(fig_practice, use_container_width=True)

with bottom_right:
    st.subheader("Usage by Hour")

    hour_data = (
        df.groupby("hour")["total_tokens"]
        .sum()
        .reset_index()
    )

    fig_hour = px.bar(hour_data, x="hour", y="total_tokens")
    st.plotly_chart(fig_hour, use_container_width=True)

st.markdown("---")

st.subheader("About This Dashboard")
st.write(
    """
    This dashboard provides an overview of Claude Code usage based on telemetry data and employee metadata.
    Use the sidebar to navigate between pages and apply filters for practice, level, location, and model.
    """
)
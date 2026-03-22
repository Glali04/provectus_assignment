import streamlit as st
import plotly.express as px

from utils.load_from_db import load_usage_data
from utils.filters import apply_filters

st.set_page_config(layout="wide")
st.title("📊 Overview")

df = load_usage_data()

if df.empty:
    st.warning("No data found in the database.")
    st.stop()

df = apply_filters(df)

if df.empty:
    st.warning("No data matches the selected filters.")
    st.stop()

# KPI cards
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Tokens", f"{int(df['total_tokens'].sum()):,}")
col2.metric("Active Users", int(df["email"].nunique()))
col3.metric("Sessions", int(df["session_id"].nunique()))
col4.metric("Total Cost ($)", f"{df['cost_usd'].sum():.2f}")
col5.metric("Avg Duration (ms)", f"{df['duration_ms'].mean():.2f}")

st.markdown("---")

# Token usage over time
st.subheader("Token Usage Over Time")

trend = (
    df.groupby("date")["total_tokens"]
    .sum()
    .reset_index()
)

fig_trend = px.line(trend, x="date", y="total_tokens")
st.plotly_chart(fig_trend, use_container_width=True)

st.caption("Insight: This shows how total token consumption changes over time.")

# Daily cost trend
st.subheader("Daily Cost Trend")

daily_cost = (
    df.groupby("date")["cost_usd"]
    .sum()
    .reset_index()
)

fig_cost = px.line(daily_cost, x="date", y="cost_usd")
st.plotly_chart(fig_cost, use_container_width=True)

st.caption("Insight: This highlights how usage translates into cost over time.")

# Requests by hour
st.subheader("Requests by Hour")

requests_by_hour = (
    df.groupby("hour")
    .size()
    .reset_index(name="request_count")
)

fig_requests = px.bar(requests_by_hour, x="hour", y="request_count")
st.plotly_chart(fig_requests, use_container_width=True)

st.caption("Insight: This identifies the busiest hours of the day.")
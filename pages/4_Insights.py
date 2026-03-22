import streamlit as st
import plotly.express as px

from utils.load_from_db import load_usage_data
from utils.filters import apply_filters

st.set_page_config(layout="wide")
st.title("🧠 Insights")

df = load_usage_data()

if df.empty:
    st.warning("No data found in the database.")
    st.stop()

df = apply_filters(df)

if df.empty:
    st.warning("No data matches the selected filters.")
    st.stop()

# Top users by token usage
st.subheader("Top Users by Token Usage")

top_users = (
    df.groupby(["email", "full_name", "practice"])["total_tokens"]
    .sum()
    .reset_index()
    .sort_values(by="total_tokens", ascending=False)
    .head(10)
)

st.dataframe(top_users, use_container_width=True)

fig_top_users = px.bar(top_users, x="full_name", y="total_tokens")
st.plotly_chart(fig_top_users, use_container_width=True)

st.caption("Insight: These users account for the largest share of token usage.")

# Top costly users
st.subheader("Top 10 Costliest Users")

top_cost_users = (
    df.groupby(["email", "full_name", "practice"])["cost_usd"]
    .sum()
    .reset_index()
    .sort_values(by="cost_usd", ascending=False)
    .head(10)
)

st.dataframe(top_cost_users, use_container_width=True)

st.caption("Insight: These users generate the highest total API cost.")

# Tokens per session distribution
st.subheader("Tokens per Session Distribution")

session_tokens = (
    df.groupby("session_id")["total_tokens"]
    .sum()
    .reset_index()
)

fig_session = px.histogram(session_tokens, x="total_tokens", nbins=30)
st.plotly_chart(fig_session, use_container_width=True)

st.caption("Insight: Most sessions are usually small, while a few are much larger.")

# Top sessions by total tokens
st.subheader("Top Sessions by Total Tokens")

top_sessions = (
    df.groupby("session_id")
    .agg(
        total_tokens=("total_tokens", "sum"),
        total_cost=("cost_usd", "sum"),
        request_count=("id", "count")
    )
    .reset_index()
    .sort_values(by="total_tokens", ascending=False)
    .head(10)
)

st.dataframe(top_sessions, use_container_width=True)

st.caption("Insight: These sessions consumed the most resources.")

# Slowest requests
st.subheader("Slowest Requests")

slowest_requests = (
    df.sort_values(by="duration_ms", ascending=False)
    [["timestamp", "email", "full_name", "model", "duration_ms", "total_tokens", "cost_usd"]]
    .head(20)
)

st.dataframe(slowest_requests, use_container_width=True)

st.caption("Insight: These requests had the highest latency.")

# Cost vs token usage
st.subheader("Cost vs Total Tokens")

fig_scatter = px.scatter(
    df,
    x="total_tokens",
    y="cost_usd",
    hover_data=["email", "full_name", "practice", "model"]
)

st.plotly_chart(fig_scatter, use_container_width=True)

st.caption("Insight: Cost generally increases with token usage, but model choice also matters.")

# Anomalies
st.subheader("Anomalies")

threshold = df["total_tokens"].mean() + 2 * df["total_tokens"].std()
anomalies = df[df["total_tokens"] > threshold]

st.dataframe(
    anomalies[[
        "timestamp",
        "email",
        "full_name",
        "practice",
        "model",
        "total_tokens",
        "cost_usd",
        "duration_ms"
    ]],
    use_container_width=True
)

st.caption("Insight: These requests are unusually large compared to the dataset average.")
import streamlit as st
import plotly.express as px

from utils.load_from_db import load_usage_data
from utils.filters import apply_filters

st.set_page_config(layout="wide")
st.title("📈 Usage Analysis")

df = load_usage_data()

if df.empty:
    st.warning("No data found in the database.")
    st.stop()

df = apply_filters(df)

if df.empty:
    st.warning("No data matches the selected filters.")
    st.stop()

# Tokens by practice
st.subheader("Tokens by Practice")

practice_data = (
    df.groupby("practice")["total_tokens"]
    .sum()
    .reset_index()
    .sort_values(by="total_tokens", ascending=False)
)

fig_practice = px.bar(practice_data, x="practice", y="total_tokens")
st.plotly_chart(fig_practice, use_container_width=True)

st.caption("Insight: This shows which engineering practices consume the most tokens.")

# Tokens by level
st.subheader("Tokens by Level")

level_data = (
    df.groupby("level")["total_tokens"]
    .sum()
    .reset_index()
    .sort_values(by="level")
)

fig_level = px.bar(level_data, x="level", y="total_tokens")
st.plotly_chart(fig_level, use_container_width=True)

st.caption("Insight: This compares usage across employee seniority levels.")

# Tokens by location
st.subheader("Tokens by Location")

location_data = (
    df.groupby("location")["total_tokens"]
    .sum()
    .reset_index()
    .sort_values(by="total_tokens", ascending=False)
)

fig_location = px.bar(location_data, x="location", y="total_tokens")
st.plotly_chart(fig_location, use_container_width=True)

st.caption("Insight: This reveals where usage is geographically concentrated.")

# Usage by hour
st.subheader("Usage by Hour")

hour_data = (
    df.groupby("hour")["total_tokens"]
    .sum()
    .reset_index()
)

fig_hour = px.bar(hour_data, x="hour", y="total_tokens")
st.plotly_chart(fig_hour, use_container_width=True)

st.caption("Insight: This shows at which hours token usage is highest.")

# Model usage by total tokens
st.subheader("Model Usage by Total Tokens")

model_tokens = (
    df.groupby("model")["total_tokens"]
    .sum()
    .reset_index()
    .sort_values(by="total_tokens", ascending=False)
)

fig_model_tokens = px.bar(model_tokens, x="model", y="total_tokens")
st.plotly_chart(fig_model_tokens, use_container_width=True)

st.caption("Insight: This shows which models drive the most token consumption.")

# Average request duration by model
st.subheader("Average Request Duration by Model")

model_duration = (
    df.groupby("model")["duration_ms"]
    .mean()
    .reset_index()
    .sort_values(by="duration_ms", ascending=False)
)

fig_model_duration = px.bar(model_duration, x="model", y="duration_ms")
st.plotly_chart(fig_model_duration, use_container_width=True)

st.caption("Insight: This compares performance across different models.")
import streamlit as st
import pandas as pd


def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    st.sidebar.markdown("---")
    st.sidebar.header("Filters")

    practices = ["All"] + sorted(df["practice"].dropna().unique().tolist()) if "practice" in df.columns else ["All"]
    levels = ["All"] + sorted(df["level"].dropna().unique().tolist()) if "level" in df.columns else ["All"]
    locations = ["All"] + sorted(df["location"].dropna().unique().tolist()) if "location" in df.columns else ["All"]
    models = ["All"] + sorted(df["model"].dropna().unique().tolist()) if "model" in df.columns else ["All"]

    selected_practice = st.sidebar.selectbox("Practice", practices)
    selected_level = st.sidebar.selectbox("Level", levels)
    selected_location = st.sidebar.selectbox("Location", locations)
    selected_model = st.sidebar.selectbox("Model", models)

    if selected_practice != "All":
        df = df[df["practice"] == selected_practice]

    if selected_level != "All":
        df = df[df["level"] == selected_level]

    if selected_location != "All":
        df = df[df["location"] == selected_location]

    if selected_model != "All":
        df = df[df["model"] == selected_model]

    return df
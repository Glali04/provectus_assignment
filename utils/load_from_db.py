import sqlite3
import pandas as pd


DB_PATH = "data/analytics.db"


def load_usage_data() -> pd.DataFrame:
    conn = sqlite3.connect(DB_PATH)

    query = """
        SELECT
            a.id,
            a.email,
            a.session_id,
            a.timestamp,
            a.input_tokens,
            a.output_tokens,
            a.total_tokens,
            a.cost_usd,
            a.duration_ms,
            a.model,
            a.terminal_type,
            e.full_name,
            e.practice,
            e.level,
            e.location
        FROM api_requests a
        LEFT JOIN employees e
            ON a.email = e.email
    """

    df = pd.read_sql(query, conn)
    conn.close()

    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df["hour"] = df["timestamp"].dt.hour
    df["date"] = df["timestamp"].dt.date

    return df
import sqlite3
import pandas as pd


def create_connection(db_path: str) -> sqlite3.Connection:
    """
    Create and return a SQLite connection.
    """
    return sqlite3.connect(db_path)


def create_tables(conn: sqlite3.Connection) -> None:
    """
    Create employees and api_requests tables.
    """
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            email TEXT PRIMARY KEY,
            full_name TEXT,
            practice TEXT,
            level TEXT,
            location TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS api_requests (
            id TEXT PRIMARY KEY,
            email TEXT NOT NULL,
            session_id TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            input_tokens INTEGER NOT NULL,
            output_tokens INTEGER NOT NULL,
            total_tokens INTEGER NOT NULL,
            cost_usd REAL NOT NULL,
            duration_ms INTEGER NOT NULL,
            model TEXT,
            terminal_type TEXT,
            FOREIGN KEY (email) REFERENCES employees(email)
        )
    """)

    conn.commit()


def insert_employees(conn: sqlite3.Connection, employees_df: pd.DataFrame) -> None:
    cursor = conn.cursor()
    records = employees_df.to_dict(orient="records")

    cursor.executemany("""
        INSERT OR REPLACE INTO employees (
            email, full_name, practice, level, location
        )
        VALUES (
            :email, :full_name, :practice, :level, :location
        )
    """, records)

    conn.commit()


def insert_api_requests(conn: sqlite3.Connection, api_df: pd.DataFrame) -> None:
    """
    Insert api requests into the database, ignoring duplicates by primary key.
    """
    cursor = conn.cursor()

    records = api_df.to_dict(orient="records")

    cursor.executemany("""
        INSERT OR IGNORE INTO api_requests (
            id, email, session_id, timestamp,
            input_tokens, output_tokens, total_tokens,
            cost_usd, duration_ms, model, terminal_type
        )
        VALUES (
            :id, :email, :session_id, :timestamp,
            :input_tokens, :output_tokens, :total_tokens,
            :cost_usd, :duration_ms, :model, :terminal_type
        )
    """, records)

    conn.commit()
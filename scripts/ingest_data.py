from utils.parse_telemetry import parse_api_requests
from utils.load_employees import load_employees
from utils.database import (
    create_connection,
    create_tables,
    insert_employees,
    insert_api_requests
)


def run_ingestion():
    api_df = parse_api_requests("data/telemetry_logs.jsonl")
    employees_df = load_employees("data/employees.csv")

    api_df["timestamp"] = api_df["timestamp"].astype(str)

    conn = create_connection("data/analytics.db")

    try:
        create_tables(conn)
        insert_employees(conn, employees_df)
        insert_api_requests(conn, api_df)
        print("Data ingestion finished successfully.")
    finally:
        conn.close()


if __name__ == "__main__":
    run_ingestion()
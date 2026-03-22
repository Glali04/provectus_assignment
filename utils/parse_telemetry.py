import pandas as pd
import json

def parse_api_requests(file_path: str) -> pd.DataFrame:
    """
        Parse telemetry JSONL file and extract only api_request events.
        Returns a clean pandas DataFrame.
        """

    rows = []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    batch = json.loads(line)

                    for event in batch.get("logEvents", []):

                        if not event.get("id"):
                            continue

                        try:
                            message = json.loads(event["message"])
                            attrs = message.get("attributes", {})

                            # Only keep api_request events
                            if message.get("body") != "claude_code.api_request":
                                continue

                            row = {
                                "id": event.get("id"),
                                "email": attrs.get("user.email"),
                                "session_id": attrs.get("session.id"),
                                "timestamp": attrs.get("event.timestamp"),
                                "input_tokens": attrs.get("input_tokens"),
                                "output_tokens": attrs.get("output_tokens"),
                                "cost_usd": attrs.get("cost_usd"),
                                "duration_ms": attrs.get("duration_ms"),
                                "model": attrs.get("model"),
                                "terminal_type": attrs.get("terminal.type"),
                            }

                            rows.append(row)

                        except (json.JSONDecodeError, KeyError):
                            # Skip broken events
                            continue

                except json.JSONDecodeError:
                    # Skip broken lines
                    continue

    except FileNotFoundError:
        raise Exception(f"File not found: {file_path}")

    # Convert to DataFrame
    df = pd.DataFrame(rows)

    if df.empty:
        return df

    # 🧹 CLEANING / TYPE CONVERSION

    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    df["input_tokens"] = pd.to_numeric(df["input_tokens"], errors="coerce")
    df["output_tokens"] = pd.to_numeric(df["output_tokens"], errors="coerce")
    df["cost_usd"] = pd.to_numeric(df["cost_usd"], errors="coerce")
    df["duration_ms"] = pd.to_numeric(df["duration_ms"], errors="coerce")

    # Derived column
    df["total_tokens"] = df["input_tokens"] + df["output_tokens"]

    # Drop invalid rows
    df = df.dropna(subset=[
        "id",
        "email",
        "timestamp",
        "session_id",
        "input_tokens",
        "output_tokens",
        "cost_usd"
    ])

    # Remove invalid numeric values
    df = df[
        (df["input_tokens"] >= 0) &
        (df["output_tokens"] >= 0) &
        (df["cost_usd"] >= 0)
    ]

    return df
import pandas as pd

def load_employees(file_path: str) -> pd.DataFrame:
    """
    Load and clean employees.csv
    """
    df = pd.read_csv(file_path)

    # normalize column names if needed
    df.columns = df.columns.str.strip()

    # basic cleaning
    df["email"] = df["email"].astype(str).str.strip().str.lower()
    df["full_name"] = df["full_name"].astype(str).str.strip()
    df["practice"] = df["practice"].astype(str).str.strip()
    df["level"] = df["level"].astype(str).str.strip()
    df["location"] = df["location"].astype(str).str.strip()

    # remove rows without email
    df = df.dropna(subset=["email"])
    df = df[df["email"] != ""]

    # remove duplicate employees by email, keep first
    df = df.drop_duplicates(subset=["email"])

    return df
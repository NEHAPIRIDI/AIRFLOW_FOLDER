# processing/clean.py
import pandas as pd

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans raw API data using business keys
    """

    # 1. Drop duplicates using business key and FORCE copy
    df = df.drop_duplicates(subset=["id", "userId"]).copy()

    # 2. Handle missing values
    df.loc[:, "title"] = df["title"].fillna("unknown")
    df.loc[:, "body"] = df["body"].fillna("")

    # 3. Standardize text
    df.loc[:, "title"] = df["title"].str.strip().str.lower()

    # 4. Ensure correct data types
    df.loc[:, "id"] = df["id"].astype(int)
    df.loc[:, "userId"] = df["userId"].astype(int)

    return df

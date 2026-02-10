# processing/transform.py
import pandas as pd

def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Applies transformations to cleaned data
    """

    # 1. Length of title
    df["title_length"] = df["title"].str.len()

    # 2. Word count in body
    df["body_word_count"] = df["body"].apply(
        lambda x: len(x.split()) if isinstance(x, str) else 0
    )

    # 3. Simple classification
    df["title_size"] = df["title_length"].apply(
        lambda x: "short" if x < 20 else "long"
    )

    return df

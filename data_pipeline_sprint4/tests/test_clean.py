import pandas as pd
from data_pipeline_sprint4.clean import clean_data

def test_clean_data():
    raw_df = pd.DataFrame({
        "id": [1, 1],
        "userId": [10, 10],
        "title": [" Test Title ", None],
        "body": [None, "some text"]
    })

    clean_df = clean_data(raw_df)

    assert len(clean_df) == 1          # duplicates removed
    assert clean_df["title"].iloc[0] == "test title"

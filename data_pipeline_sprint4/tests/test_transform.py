import pandas as pd
from data_pipeline_sprint4.transform import transform_data

def test_transform_data():
    df = pd.DataFrame({
        "title": ["short title"],
        "body": ["this is a test body"]
    })

    result = transform_data(df)

    assert "title_length" in result.columns
    assert "body_word_count" in result.columns
    assert result["body_word_count"].iloc[0] == 5

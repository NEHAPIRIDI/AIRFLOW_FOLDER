from data_pipeline_sprint4.fetch_api import fetch_data

def test_fetch_data():
    data = fetch_data()

    assert data is not None
    assert isinstance(data, list)
    assert len(data) > 0

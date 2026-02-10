# main.py
import json
import pandas as pd

from fetch_api import fetch_data
from clean import clean_data
from transform import transform_data

def main():
    # 1. Extract
    data = fetch_data()

    # 2. Store raw data (staging)
    with open("raw_api_data.json", "w") as f:
        json.dump(data, f)

    # 3. Load to DataFrame
    df = pd.read_json("raw_api_data.json")

    # 4. Clean
    df = clean_data(df)

    # 5. Transform
    df = transform_data(df)

    print(df.head())
    print("Total records fetched:", len(data))


if __name__ == "__main__":
    main()

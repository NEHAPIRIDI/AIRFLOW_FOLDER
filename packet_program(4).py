import pandas as pd

input_file = "Amazon.csv"
output_file = "processed_output.csv"

chunk_size = 5000
first_chunk = True

for chunk in pd.read_csv(input_file, chunksize=chunk_size):

    # -----------------------------
    # TRANSFORMATION (example)
    # -----------------------------
    # 1. Drop rows with missing values
    chunk = chunk.dropna()

    # 2. Example: convert numeric columns safely
    for col in chunk.select_dtypes(include="object").columns:
        chunk[col] = chunk[col].astype(str)

    # -----------------------------
    # LOAD STEP
    # -----------------------------
    chunk.to_csv(
        output_file,
        mode="a",
        index=False,
        header=first_chunk
    )

    first_chunk = False
    print(f"Processed {len(chunk)} rows")

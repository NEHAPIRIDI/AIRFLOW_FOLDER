import pandas as pd
import os

input_file = "Amazon.csv"
output_dir = "output_chunks"

chunk_size = 5000

# Create output directory if not exists
os.makedirs(output_dir, exist_ok=True)

chunk_number = 1

for chunk in pd.read_csv(input_file, chunksize=chunk_size):

    # -----------------------------
    # TRANSFORMATION
    # -----------------------------
    # Drop rows with NULL values
    chunk = chunk.dropna()

    # Convert object columns safely
    for col in chunk.select_dtypes(include="object").columns:
        chunk[col] = chunk[col].astype(str)

    # -----------------------------
    # LOAD STEP (One file per chunk)
    # -----------------------------
    output_file = os.path.join(output_dir, f"chunk_{chunk_number}.csv")

    chunk.to_csv(
        output_file,
        index=False
    )

    print(f"Chunk {chunk_number} processed and saved ({len(chunk)} rows)")

    chunk_number += 1

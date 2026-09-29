
import pandas as pd
import numpy as np
from pathlib import Path

dataset_folder = Path("dataset")
csv_files = sorted(dataset_folder.rglob("*.csv"))

output_folder = Path("dataset/processed")
output_folder.mkdir(parents=True, exist_ok=True)

output_file = output_folder / "cleaned_data.csv"

if output_file.exists():
    output_file.unlink()

first_chunk = True

for file in csv_files:
    print(f"Processing: {file.name}")

    for chunk in pd.read_csv(file, chunksize=50000, low_memory=False):
        chunk.columns = chunk.columns.str.strip()

        if "Label" not in chunk.columns:
            print("Skipping file: Label column missing")
            break

        chunk = chunk.replace([np.inf, -np.inf], np.nan)
        chunk = chunk.dropna()
        chunk["Label"] = chunk["Label"].astype(str).str.strip()

        chunk.to_csv(
            output_file,
            mode="w" if first_chunk else "a",
            header=first_chunk,
            index=False
        )

        first_chunk = False

print("Preprocessing completed!")
print("Saved to:", output_file)
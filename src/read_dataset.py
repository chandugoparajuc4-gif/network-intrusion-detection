
import pandas as pd
from pathlib import Path

dataset_folder = Path("dataset")
csv_files = sorted(dataset_folder.rglob("*.csv"))

if not csv_files:
    print("No CSV files found.")
else:
    file = csv_files[0]
    print("Reading file:", file.name)

    df = pd.read_csv(file, nrows=5)
    df.columns = df.columns.str.strip()

    print("\nDataset shape (first 5 rows):")
    print(df.shape)

    print("\nColumn names:")
    print(df.columns.tolist())

    print("\nFirst 5 records:")
    print(df.to_string(index=False))

    print("\nData types:")
    print(df.dtypes)
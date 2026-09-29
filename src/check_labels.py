
import pandas as pd
from pathlib import Path

dataset_folder = Path("dataset")
csv_files = list(dataset_folder.rglob("*.csv"))

if not csv_files:
    print("No CSV files found.")
else:
    file = csv_files[0]
    print("Reading:", file.name)

    df = pd.read_csv(file, usecols=[" Label"])

    print("\nAttack label counts:")
    print(df[" Label"].value_counts())

    print("\nTotal records:", len(df))
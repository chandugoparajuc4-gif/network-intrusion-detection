
import pandas as pd
from pathlib import Path

file = Path("dataset/processed/cleaned_data.csv")

if not file.exists():
    print("Cleaned dataset not found!")
else:
    df = pd.read_csv(file, nrows=10000, low_memory=False)

    print("Dataset file found!")
    print("Columns:", len(df.columns))
    print("Rows checked:", len(df))

    print("\nMissing values:")
    print(df.isnull().sum().sum())

    print("\nAttack labels in first 10000 rows:")
    print(df["Label"].value_counts())

    print("\nFirst 5 rows:")
    print(df.head())
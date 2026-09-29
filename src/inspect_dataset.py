
from pathlib import Path
import pandas as pd

dataset_folder = Path("dataset")
csv_files = list(dataset_folder.rglob("*.csv"))

print("Number of CSV files:", len(csv_files))

for file in csv_files:
    print(file)
import pandas as pd
from pathlib import Path

file = Path("dataset/processed/cleaned_data.csv")

if not file.exists():
    print("Cleaned dataset not found!")
else:
    label_counts = {}

    for chunk in pd.read_csv(file, chunksize=50000, low_memory=False):
        counts = chunk["Label"].value_counts()

        for label, count in counts.items():
            label_counts[label] = label_counts.get(label, 0) + count

    print("\nTotal records:", sum(label_counts.values()))
    print("\nAttack label counts:")

    for label, count in sorted(label_counts.items()):
        print(f"{label}: {count}")

    print("\nTotal labels:", len(label_counts))
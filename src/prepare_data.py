
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

input_file = Path("dataset/processed/cleaned_data.csv")
output_folder = Path("dataset/processed")
output_folder.mkdir(parents=True, exist_ok=True)

print("Loading dataset...")

df = pd.read_csv(input_file, low_memory=False)

print("Dataset loaded!")
print("Shape:", df.shape)

df.columns = df.columns.str.strip()
df = df.loc[:, ~df.columns.duplicated()]

df["Label"] = df["Label"].astype(str).str.strip()

X = df.drop(columns=["Label"])
y = df["Label"]

encoder = LabelEncoder()
y = encoder.fit_transform(y)

print("Labels:", list(encoder.classes_))

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

X_train = X_train.replace([float("inf"), float("-inf")], 0)
X_test = X_test.replace([float("inf"), float("-inf")], 0)

X_train = X_train.fillna(0)
X_test = X_test.fillna(0)

X_train.to_csv(output_folder / "X_train.csv", index=False)
X_test.to_csv(output_folder / "X_test.csv", index=False)
pd.Series(y_train).to_csv(output_folder / "y_train.csv", index=False)
pd.Series(y_test).to_csv(output_folder / "y_test.csv", index=False)

print("Training and testing data saved!")
print("Training rows:", len(X_train))
print("Testing rows:", len(X_test))
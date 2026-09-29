
import pandas as pd
import joblib
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder

data_folder = Path("dataset/processed")
model_folder = Path("models")
model_folder.mkdir(parents=True, exist_ok=True)

print("Loading training data...")

X_train = pd.read_csv(data_folder / "X_train.csv")
X_test = pd.read_csv(data_folder / "X_test.csv")
y_train = pd.read_csv(data_folder / "y_train.csv").iloc[:, 0]
y_test = pd.read_csv(data_folder / "y_test.csv").iloc[:, 0]

print("Training data:", X_train.shape)
print("Testing data:", X_test.shape)

print("Training Random Forest model...")

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    n_jobs=-1,
    class_weight="balanced"
)

model.fit(X_train, y_train)

print("Model training completed!")

print("Predicting test data...")
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("\nModel Accuracy:", accuracy)
print("\nClassification Report:")
print(classification_report(y_test, y_pred, zero_division=0))

model_path = model_folder / "intrusion_detection_model.pkl"
joblib.dump(model, model_path)

print("\nModel saved to:", model_path)
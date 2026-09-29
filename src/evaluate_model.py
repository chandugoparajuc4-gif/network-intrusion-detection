
import pandas as pd
import joblib
from pathlib import Path
from sklearn.metrics import (
    confusion_matrix,
    classification_report,
    ConfusionMatrixDisplay
)
import matplotlib.pyplot as plt

data_folder = Path("dataset/processed")
model_path = Path("models/intrusion_detection_model.pkl")

print("Loading trained model...")
model = joblib.load(model_path)

print("Loading test data...")
X_test = pd.read_csv(data_folder / "X_test.csv")
y_test = pd.read_csv(data_folder / "y_test.csv").iloc[:, 0]

print("Generating predictions...")
y_pred = model.predict(X_test)

print("\nClassification Report:")
print(classification_report(y_test, y_pred, zero_division=0))

print("\nConfusion Matrix:")
cm = confusion_matrix(y_test, y_pred)
print(cm)

print("\nGenerating confusion matrix image...")
display = ConfusionMatrixDisplay(confusion_matrix=cm)
display.plot(
    xticks_rotation="vertical",
    cmap="Blues",
    values_format="d"
)
plt.title("Network Intrusion Detection - Confusion Matrix")
plt.tight_layout()

output_path = Path("models/confusion_matrix.png")
plt.savefig(output_path, dpi=300)
plt.close()

print("Confusion matrix saved to:", output_path)
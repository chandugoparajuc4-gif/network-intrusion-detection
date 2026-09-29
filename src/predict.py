
import pandas as pd
import joblib
from pathlib import Path

MODEL_PATH = Path("models/intrusion_detection_model.pkl")
TEST_DATA_PATH = Path("dataset/processed/X_test.csv")

def predict_traffic(data):
    model = joblib.load(MODEL_PATH)

    if isinstance(data, dict):
        data = pd.DataFrame([data])

    prediction = model.predict(data)[0]

    labels = [
        "BENIGN",
        "Bot",
        "DDoS",
        "DoS GoldenEye",
        "DoS Hulk",
        "DoS Slowhttptest",
        "DoS slowloris",
        "FTP-Patator",
        "Heartbleed",
        "Infiltration",
        "PortScan",
        "SSH-Patator",
        "Web Attack � Brute Force",
        "Web Attack � Sql Injection",
        "Web Attack � XSS"
    ]

    return labels[int(prediction)]


if __name__ == "__main__":
    print("Loading test data...")

    data = pd.read_csv(TEST_DATA_PATH, nrows=1)

    print("Predicting network traffic...")
    result = predict_traffic(data)

    print("\nPrediction result:", result)

    if result == "BENIGN":
        print("Status: Normal traffic")
    else:
        print("Status: Potential attack detected")
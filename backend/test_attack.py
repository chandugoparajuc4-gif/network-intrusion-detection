
import pandas as pd
import requests

X_file = "dataset/processed/X_test.csv"
y_file = "dataset/processed/y_test.csv"

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

print("Searching for an attack record...")

x_chunks = pd.read_csv(X_file, chunksize=50000)
y_chunks = pd.read_csv(y_file, chunksize=50000)

for X_chunk, y_chunk in zip(x_chunks, y_chunks):
    attack_rows = y_chunk.iloc[:, 0] != 0

    if attack_rows.any():
        index = attack_rows[attack_rows].index[0]
        position = y_chunk.index.get_loc(index)

        payload = X_chunk.iloc[position].to_dict()
        actual = int(y_chunk.iloc[position, 0])

        print("Actual attack:", labels[actual])
        print("Sending record to API...")

        response = requests.post(
            "http://127.0.0.1:5000/predict",
            json=payload
        )

        print("Status code:", response.status_code)
        print("Model response:", response.json())
        break
else:
    print("No attack record found.")
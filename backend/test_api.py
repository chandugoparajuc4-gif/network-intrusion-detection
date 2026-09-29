import pandas as pd
import requests

data = pd.read_csv(
    "dataset/processed/X_test.csv",
    nrows=1
)

payload = data.iloc[0].to_dict()

response = requests.post(
    "http://127.0.0.1:5000/predict",
    json=payload
)

print("Status code:", response.status_code)
print("Prediction:", response.json())
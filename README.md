# AI-Based Network Intrusion Detection System

## Project Overview
The AI-Based Network Intrusion Detection System is a machine learning project that classifies network traffic and identifies potential network attacks. It uses the CIC-IDS2017 dataset and a Random Forest classifier.

The project includes a Flask backend, a web-based dashboard, and an SQLite database for storing prediction history.

**Note:** This project analyzes supplied network traffic features. It does not currently capture live network packets.

## Features
- Network traffic classification using a trained Random Forest model.
- Classification of normal traffic and multiple attack categories.
- Web dashboard with 78 network traffic input features.
- Sample data loading for testing.
- Prediction history stored in SQLite.
- Dashboard statistics for total predictions, normal traffic, and detected attacks.
- REST API built with Flask.

## Technologies Used
- Python
- Pandas and NumPy
- Scikit-learn
- Flask and Flask-CORS
- SQLite
- HTML, CSS, and JavaScript
- CIC-IDS2017 dataset

## Project Structure
```
network-intrusion-detection/
│
├── backend/
│   ├── app.py
│   ├── routes.py
│   └── test_attack.py
│
├── dataset/
│   ├── MachineLearningCVE/
│   └── processed/
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── models/
│   └── intrusion_detection_model.pkl
│
├── src/
│   ├── preprocessing.py
│   ├── prepare_data.py
│   └── train_model.py
│
├── venv/
├── requirements.txt
├── README.md
└── .gitignore
```

*The database and model files are generated locally. The exact contents of folders may vary.*

## Dataset
This project uses the CIC-IDS2017 dataset, which contains labeled network traffic for benign activity and different attack types.

The model uses 78 network traffic features. The dataset is split into training and testing data before model training.

## Model
A Random Forest classifier is trained to predict the network traffic category.

The model supports these classes:
- BENIGN
- Bot
- DDoS
- DoS GoldenEye
- DoS Hulk
- DoS Slowhttptest
- DoS slowloris
- FTP-Patator
- Heartbleed
- Infiltration
- PortScan
- SSH-Patator
- Web Attack - Brute Force
- Web Attack - Sql Injection
- Web Attack - XSS

The recorded test accuracy was approximately 99.85%, with a macro-average F1-score of approximately 0.88. Because the dataset is imbalanced and some attack classes have very few test examples, accuracy alone does not represent performance equally across all classes.

These results are from the prepared test dataset, not from live network monitoring.

## Installation

### 1. Clone the repository
```bash
git clone <your-github-repository-url>
cd network-intrusion-detection
```

### 2. Create a virtual environment
On Windows PowerShell:
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies
```powershell
pip install -r requirements.txt
```

### 4. Prepare the dataset and model
Place the CIC-IDS2017 CSV files in the dataset folder. Run the preprocessing, data preparation, and training scripts in the order used in this project.

```powershell
python src/preprocessing.py
python src/prepare_data.py
python src/train_model.py
```

Make sure the scripts and dataset files are in the expected locations before running them.

## Run the Application
Start the Flask backend from the project root:

```powershell
python backend/app.py
```

Open the frontend using VS Code Live Server. For example:

```text
http://127.0.0.1:5500/frontend/index.html
```

Keep the Flask backend running while using the dashboard.

## API Endpoints
| Method | Endpoint | Purpose |
|---|---|---|
| GET | / | Check whether the API is running |
| GET | /features | Get the model feature names |
| GET | /sample | Get a sample traffic record |
| POST | /predict | Classify a traffic record |
| GET | /history | View recent predictions |
| GET | /stats | View prediction statistics |

The prediction endpoint expects a JSON object containing all required model features.

## Testing
Run the attack test from the project root:

```powershell
python backend/test_attack.py
```

The test sends an attack record to the prediction API and checks the returned classification. The dashboard can also be tested by loading sample data and analyzing it.

## Limitations
- The current system classifies feature records supplied to its API; it does not capture live packets.
- Model performance depends on the dataset and the quality of the input features.
- Some attack categories have limited test examples.
- This is an educational and demonstration project, not a replacement for a production network security system.

## Future Enhancements
- Integrate live packet capture.
- Add real-time traffic monitoring.
- Improve detection of rare attack categories.
- Add visual charts and downloadable reports.
- Deploy the application to a cloud server.

## Author
Chandu Goparaju

## License
For educational and project demonstration purposes.
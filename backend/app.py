
from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import sqlite3
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "intrusion_detection_model.pkl"
DB_PATH = BASE_DIR / "backend" / "predictions.db"

app = Flask(__name__)
CORS(app)

# Load trained model
model = joblib.load(MODEL_PATH)

# Get feature names
feature_names = list(model.feature_names_in_)

# Attack labels
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
    "Web Attack - Brute Force",
    "Web Attack - Sql Injection",
    "Web Attack - XSS"
]


# Initialize SQLite database
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prediction TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)


init_db()


# Home route
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "AI Network Intrusion Detection API is running"
    })


# Get model features
@app.route("/features", methods=["GET"])
def features():
    return jsonify({
        "features": feature_names
    })


# Load one sample row from X_test.csv
@app.route("/sample", methods=["GET"])
def sample():
    try:
        sample_path = (
            BASE_DIR / "dataset" / "processed" / "X_test.csv"
        )

        data = pd.read_csv(sample_path, nrows=1)
        sample_data = data.iloc[0].to_dict()

        return jsonify(sample_data)

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# Predict network traffic
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        if not isinstance(data, dict):
            return jsonify({
                "error": "Please provide network traffic data as JSON"
            }), 400

        # Check missing features
        missing = [
            name for name in feature_names
            if name not in data
        ]

        if missing:
            return jsonify({
                "error": "Missing features",
                "missing": missing
            }), 400

        # Create DataFrame in training feature order
        row = pd.DataFrame(
            [[data[name] for name in feature_names]],
            columns=feature_names
        )

        # Convert values to numbers
        row = row.apply(pd.to_numeric, errors="raise")

        # Replace infinity and missing values
        row = row.replace(
            [float("inf"), float("-inf")],
            0
        )
        row = row.fillna(0)

        # Make prediction
        prediction = int(model.predict(row)[0])

        # Convert numeric prediction to label
        if prediction < 0 or prediction >= len(labels):
            return jsonify({
                "error": "Invalid prediction class"
            }), 500

        prediction_name = labels[prediction]

        status = (
            "Normal traffic"
            if prediction_name == "BENIGN"
            else "Potential attack detected"
        )

        # Save prediction in SQLite database
        created_at = datetime.now().astimezone().isoformat(
            timespec="seconds"
        )

        with sqlite3.connect(DB_PATH) as conn:
            conn.execute(
                """
                INSERT INTO predictions
                (prediction, status, created_at)
                VALUES (?, ?, ?)
                """,
                (prediction_name, status, created_at)
            )

        return jsonify({
            "prediction": prediction_name,
            "status": status
        })

    except (ValueError, TypeError) as e:
        return jsonify({
            "error": str(e)
        }), 400

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# Get the latest 50 predictions
@app.route("/history", methods=["GET"])
def get_history():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row

            rows = conn.execute(
                """
                SELECT id, prediction, status, created_at
                FROM predictions
                ORDER BY id DESC
                LIMIT 50
                """
            ).fetchall()

        return jsonify([
            dict(row) for row in rows
        ])

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# Get dashboard statistics
@app.route("/stats", methods=["GET"])
def get_stats():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            total = conn.execute(
                "SELECT COUNT(*) FROM predictions"
            ).fetchone()[0]

            normal = conn.execute(
                """
                SELECT COUNT(*)
                FROM predictions
                WHERE prediction = 'BENIGN'
                """
            ).fetchone()[0]

            attacks = total - normal

        return jsonify({
            "total_predictions": total,
            "normal_traffic": normal,
            "attacks_detected": attacks
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)
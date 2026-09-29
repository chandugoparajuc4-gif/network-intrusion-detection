
from flask import Blueprint, request, jsonify
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from src.predict import predict_traffic

routes = Blueprint("routes", __name__)

@routes.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        if not isinstance(data, dict):
            return jsonify({
                "error": "Please provide network traffic data as JSON"
            }), 400

        prediction = predict_traffic(data)

        return jsonify({
            "prediction": prediction,
            "status": (
                "Normal traffic"
                if prediction == "BENIGN"
                else "Potential attack detected"
            )
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400
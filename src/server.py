from flask import Flask, jsonify
from flask_cors import CORS
import json
import glob
from datetime import datetime

app = Flask(__name__)
CORS(app)


def load_latest_clean():
    files = sorted(glob.glob("data/clean/bitcoin_clean_*.json"))
    if not files:
        return None
    with open(files[-1], "r") as f:
        return json.load(f)

def load_latest_summary():
    today = datetime.now().strftime("%Y-%m-%d")
    path = f"data/summary/summary_{today}.txt"
    try:
        with open(path, "r") as f:
            return f.read()
    except:
        return "Summary not generated yet."

def load_anomalies():
    try:
        with open("data/anomalies.json", "r") as f:
            return json.load(f)
    except:
        return []

@app.get("/latest")
def latest():
    clean = load_latest_clean()
    summary = load_latest_summary()
    anomalies = load_anomalies()

    if not clean:
        return jsonify({"error": "No data available"}), 404

    clean["summary"] = summary
    clean["anomalies"] = anomalies

    return jsonify(clean)

if __name__ == "__main__":
    app.run(port=5000, debug=True)

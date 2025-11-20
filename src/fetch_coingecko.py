import requests
import json
import os
from datetime import datetime

LOG_FILE = "logs/fetch.log"

def log(message: str):
    """Simple logger that appends messages to logs/fetch.log"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")


def fetch_bitcoin_data():
    url = "https://api.coingecko.com/api/v3/coins/bitcoin"

    log("Starting request to CoinGecko...")

    response = requests.get(url)

    if response.status_code != 200:
        log(f"Request failed with status {response.status_code}")
        raise Exception("API request failed")

    log("Request successful!")

    data = response.json()

    # Save raw JSON
    today = datetime.now().strftime("%Y-%m-%d")
    output_path = f"data/raw/bitcoin_{today}.json"

    with open(output_path, "w") as f:
        json.dump(data, f, indent=4)

    log(f"Saved raw data to {output_path}")

    print(f"Data saved to {output_path}")


if __name__ == "__main__":
    fetch_bitcoin_data()

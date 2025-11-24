#timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
import requests
import os
import json
from dotenv import load_dotenv  
from datetime import datetime
load_dotenv()
API_URL = "https://api.coingecko.com/api/v3/coins/bitcoin"  

logfile = "logs/fetch.log"

def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(logfile, "a") as f:
        f.write(f"[{timestamp}] {msg}\n")

def fetch_bitcoin_data():
    response = requests.get(API_URL)

    if response.status_code != 200:
        log(f"ERROR: Failed to fetch data. Status code: {response.status_code}")
        return None

    data = response.json()
    today = datetime.now().strftime("%Y-%m-%d")
    output_path = f"data/raw/bitcoin_{today}.json"  
    with open(output_path, "w") as f:
        json.dump(data, f, indent=4)

    log(f"SUCCESS: Fetched data and saved to {output_path}")
    return data 
if __name__ == "__main__":
    os.makedirs("data/raw", exist_ok=True)
    fetch_bitcoin_data()    
import json
import glob
from datetime import datetime
from dotenv import load_dotenv
import os
from openai import OpenAI

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def load_today_clean_data():
    """Loads today's cleaned Bitcoin data."""
    today = datetime.now().strftime("%Y-%m-%d")
    path = f"data/clean/bitcoin_clean_{today}.json"
    
    with open(path, "r") as f:
        return json.load(f)

def load_anomalies():
    """Loads the most recent anomalies from Step 4."""
    anomalies_file = "data/anomalies.json"
    if os.path.exists(anomalies_file):
        with open(anomalies_file, "r") as f:
            return json.load(f)
    return []

def generate_summary(clean_data, anomalies):
    """Generate a natural language summary using OpenAI."""
    
    prompt = f"""
    You are a data analyst. Analyze the following cryptocurrency daily metrics 
    and write a short, clear summary.

    === Today's Clean Data ===
    {json.dumps(clean_data, indent=2)}

    === Detected Anomalies ===
    {json.dumps(anomalies, indent=2)}

    Write a concise 4–8 sentence summary explaining:
    - The overall BTC price trend today
    - How today's metrics compare to normal days
    - Any anomalies and potential reasons
    - Whether the market appears bullish, bearish, or neutral
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # fast + cheap + very good
        messages=[{"role": "user", "content": prompt}],
        max_tokens=250
    )

    return response.choices[0].message.content


def save_summary(text):
    today = datetime.now().strftime("%Y-%m-%d")
    path = f"data/summary/summary_{today}.txt"
    with open(path, "w") as f:
        f.write(text)
    print(f"Summary saved to {path}")

if __name__ == "__main__":
    clean_data = load_today_clean_data()

    # Load anomalies file if created (Step 4)
    anomalies = load_anomalies()

    summary = generate_summary(clean_data, anomalies)
    save_summary(summary)

    print("\n=== AI Summary ===\n")
    print(summary)

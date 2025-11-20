import os
from datetime import datetime

# Import all pipeline functions
from fetch_coingecko import fetch_bitcoin_data
from etl_clean import clean_bitcoin_data, save_clean_data
from anomaly_detector import load_clean_history, detect_anomalies
from ai_summary import load_today_clean_data, generate_summary, save_summary
from generate_report import generate_report

def create_folders():
    """Ensure all required folders exist."""
    os.makedirs("data/raw", exist_ok=True)
    os.makedirs("data/clean", exist_ok=True)
    os.makedirs("data/summary", exist_ok=True)
    os.makedirs("data/report", exist_ok=True)

def run_daily_pipeline():
    print("\n🚀 Starting Daily Bitcoin Data Pipeline...\n")

    create_folders()

    # STEP 1: Fetch Raw Data
    print("1️⃣ Fetching raw data from CoinGecko...")
    fetch_bitcoin_data()

    # STEP 2: Clean Data
    print("2️⃣ Cleaning data...")
    today = datetime.now().strftime("%Y-%m-%d")
    raw_path = f"data/raw/bitcoin_{today}.json"
    
    clean_data = clean_bitcoin_data(raw_path)
    save_clean_data(clean_data)

    # STEP 3: Detect anomalies
    print("3️⃣ Detecting anomalies...")
    history = load_clean_history()
    anomalies = []

    if len(history) >= 2:
        anomalies = detect_anomalies(history)

    # Save anomalies to file
    with open("data/anomalies.json", "w") as f:
        import json
        json.dump(anomalies, f, indent=4)

    print("  → Anomalies saved.")

    # STEP 4: AI Summary
    print("4️⃣ Generating AI summary...")
    clean_today = load_today_clean_data()
    summary_text = generate_summary(clean_today, anomalies)
    save_summary(summary_text)

    # STEP 5: Generate HTML Report
    print("5️⃣ Generating HTML report...")
    generate_report()

    print("\n🎉 Daily Pipeline Complete!")
    print("📄 Report saved in data/report/")
    print("🧠 AI summary saved in data/summary/")
    print("📈 Clean data saved in data/clean/")
    print("💾 Raw data saved in data/raw/")
    print("🚨 Anomaly data saved in data/anomalies.json\n")

if __name__ == "__main__":
    run_daily_pipeline()

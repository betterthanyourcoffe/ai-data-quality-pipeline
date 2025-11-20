import json
import glob
import statistics

def load_clean_history():
    """Load all cleaned bitcoin files from data/clean."""
    files = sorted(glob.glob("data/clean/bitcoin_clean_*.json"))

    history = []
    for file in files:
        with open(file, "r") as f:
            history.append(json.load(f))

    return history


def detect_anomalies(history):
    """Detect anomalies in price, volume, and market cap."""
    if len(history) < 2:
        return None  # Not enough data

    anomalies = []

    today = history[-1]
    prev = history[-2]

    today_price = today["current_price_usd"]
    prev_price = prev["current_price_usd"]

    today_vol = today["volume_24h"]
    prev_vol = prev["volume_24h"]

    today_mc = today["market_cap"]
    prev_mc = prev["market_cap"]

    # Price anomaly
    if prev_price:
        price_change = abs(today_price - prev_price) / prev_price
        if price_change > 0.10:
            anomalies.append({
                "metric": "price",
                "today": today_price,
                "yesterday": prev_price,
                "change%": round(price_change * 100, 2),
                "note": "Unusual price movement (>10%)"
            })

    # Volume anomaly
    if prev_vol:
        vol_change = abs(today_vol - prev_vol) / prev_vol
        if vol_change > 0.20:
            anomalies.append({
                "metric": "volume",
                "today": today_vol,
                "yesterday": prev_vol,
                "change%": round(vol_change * 100, 2),
                "note": "Abnormal volume change (>20%)"
            })

    # Market cap anomaly
    if prev_mc:
        mc_change = abs(today_mc - prev_mc) / prev_mc
        if mc_change > 0.10:
            anomalies.append({
                "metric": "market_cap",
                "today": today_mc,
                "yesterday": prev_mc,
                "change%": round(mc_change * 100, 2),
                "note": "Unusual market cap change (>10%)"
            })

    return anomalies


if __name__ == "__main__":
    import os
    os.makedirs("data", exist_ok=True)

    history = load_clean_history()

    if len(history) < 2:
        print("📄 Not enough historical data yet. Run again tomorrow.")
        anomalies = []
    else:
        anomalies = detect_anomalies(history)

    # Save anomalies to file
    with open("data/anomalies.json", "w") as f:
        json.dump(anomalies, f, indent=4)

    print("\n=== Anomalies Saved ===")
    print(anomalies if anomalies else "No anomalies today 🚀")

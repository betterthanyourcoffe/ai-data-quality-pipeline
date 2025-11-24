import json
from datetime import datetime

def clean_bitcoin_data(raw_json_path):
    """Extract useful fields from the raw CoinGecko JSON."""

    with open(raw_json_path, "r") as f:
        data = json.load(f)#creates a python dictionary from the json file

    # Extract fields safely using .get()
    market_data = data.get("market_data", {})

    clean_record = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "coin": data.get("id", "bitcoin"),
        "current_price_usd": market_data.get("current_price", {}).get("usd"),
        "market_cap": market_data.get("market_cap", {}).get("usd"),
        "volume_24h": market_data.get("total_volume", {}).get("usd"),
        "price_change_percentage_24h": market_data.get("price_change_percentage_24h"),
    }

    return clean_record


def save_clean_data(clean_data):
    """Save cleaned data to data/clean folder."""
    date = clean_data["date"]
    output_file = f"data/clean/bitcoin_clean_{date}.json"

    with open(output_file, "w") as f:
        json.dump(clean_data, f, indent=4)

    print(f"Clean data saved to {output_file}")


if __name__ == "__main__":
    today = datetime.now().strftime("%Y-%m-%d")
    raw_path = f"data/raw/bitcoin_{today}.json"

    cleaned = clean_bitcoin_data(raw_path)
    save_clean_data(cleaned)

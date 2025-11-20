import json
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
import os


def load_clean_data():
    today = datetime.now().strftime("%Y-%m-%d")
    with open(f"data/clean/bitcoin_clean_{today}.json", "r") as f:
        return json.load(f)

def load_anomalies():
    anomalies_file = "data/anomalies.json"
    if not os.path.exists(anomalies_file):
        return []
    with open(anomalies_file, "r") as f:
        return json.load(f)

def load_summary():
    today = datetime.now().strftime("%Y-%m-%d")
    with open(f"data/summary/summary_{today}.txt", "r") as f:
        return f.read()

def generate_report():
    clean_data = load_clean_data()
    anomalies = load_anomalies()
    summary = load_summary()
    today = datetime.now().strftime("%Y-%m-%d")
    
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("report.html.jinja2")

    output_html = template.render(
        date=today,
        clean_data=clean_data,
        anomalies=anomalies,
        summary=summary
    )

    output_path = f"data/report/report_{today}.html"
    with open(output_path, "w") as f:
        f.write(output_html)

    print(f"Report generated at: {output_path}")


if __name__ == "__main__":
    import os
    os.makedirs("data/report", exist_ok=True)
    generate_report()


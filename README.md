📊 AI-Powered Bitcoin Data Quality Pipeline
Automated ETL • Anomaly Detection • AI Insights • Daily Reports • GitHub Actions

This project is a complete production-style data engineering pipeline that automatically ingests Bitcoin market data daily, cleans and validates it, detects anomalies, generates AI-powered insights using LLMs, and produces a structured HTML report.
All processing runs automatically in the cloud via GitHub Actions.

🚀 Features
✅ Daily Automated ETL

Fetches Bitcoin data from CoinGecko API

Raw JSON saved in data/raw/

✅ Data Cleaning & Transform

Extracts:

USD price

24h volume

Market cap

24h % change

Timestamp
Cleaned data stored in data/clean/

✅ Anomaly Detection

Rules-based anomaly checks:

Price jumps >10%

Volume spikes >20%

Market cap changes >10%

Missing or inconsistent data
Results saved to data/anomalies.json

🧠 AI Insights (OpenAI)

Uses gpt-4o-mini to:

Summarize daily market conditions

Explain anomalies

Give sentiment analysis (bullish/bearish/neutral)
Saved to: data/summary/summary_YYYY-MM-DD.txt

📄 Daily HTML Report

Includes:

Clean dataset

Detected anomalies

AI summary

Automatic formatting via Jinja2 template
Output saved to:
data/report/report_YYYY-MM-DD.html

☁️ Cloud Automation (GitHub Actions)

Runs every day at 12:00 UTC:

Executes full ETL pipeline

Generates report

Uploads output as a downloadable artifact

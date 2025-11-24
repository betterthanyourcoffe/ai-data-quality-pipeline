# AI-Powered Bitcoin Data Quality Pipeline

Automated ETL • Anomaly Detection • AI Insights • Daily Reports

This repository implements a lightweight, production-oriented data pipeline that:

- Fetches Bitcoin market data from CoinGecko
- Cleans and normalizes the daily snapshot
- Runs simple rules-based anomaly detection
- Generates an AI summary using OpenAI
- Produces an HTML report (Jinja2 template)
- Optionally sends a daily email with the report attached

The codebase is intentionally small and modular so you can run locally, iterate on models/heuristics, or wire it into CI/cloud automation.

## Quick status

- Language: Python
- Main directory: `src/`
- Data: `data/raw/`, `data/clean/`, `data/summary/`, `data/report/`

## Features

- Daily ETL: `src/fetch_coingecko.py` fetches the raw CoinGecko JSON for Bitcoin.
- Cleaning: `src/etl_clean.py` extracts the useful fields (price, volume, market cap, etc.).
- Anomaly detection: `src/anomaly_detector.py` compares today vs yesterday and flags large changes.
- AI Summary: `src/ai_summary.py` uses OpenAI to create a brief market summary.
- HTML Report: `src/generate_report.py` renders a Jinja2 template (`templates/report.html.jinja2`).
- Email alerts: `src/email_alert.py` can send the summary + report via SMTP (configurable by env vars).
- Lightweight server: `src/server.py` exposes `/latest` to read the most recent artifacts.

## Requirements

- Python 3.10+ recommended
- See `requirements.txt` for the minimal Python packages used by the project.

## Setup (local)

1. Clone the repo and change directory:

```bash
git clone <repo-url>
cd ai-data-quality-system
```

2. Create and activate a virtual environment (macOS / zsh):

```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Configure environment variables. Create a `.env` file at the repo root with the following (example):

```env
# OpenAI (required for AI summary)
OPENAI_API_KEY=sk-...

# Email (only required if you want email alerts)
EMAIL_FROM=sender@example.com
EMAIL_PASSWORD=your-smtp-password
EMAIL_TO=recipient@example.com
SMTP_SERVER=smtp.example.com
SMTP_PORT=587
```

Notes:

- The CoinGecko public API used by `src/fetch_coingecko.py` does not require an API key.
- If you don't provide email env vars, the pipeline will still run but email sending will fail; you can disable that step if preferred.

## Run the pipeline

- Run the full daily pipeline (fetch, clean, detect, summarize, report, email):

```bash
python src/run_daily.py
```

- Run individual steps if you prefer:

- Fetch raw data only:

```bash
python src/fetch_coingecko.py
```

- Clean today's raw file:

```bash
python src/etl_clean.py
```

- Detect anomalies (requires at least 2 clean files):

```bash
python src/anomaly_detector.py
```

- Generate AI summary (requires OpenAI key):

```bash
python src/ai_summary.py
```

- Generate HTML report:

```bash
python src/generate_report.py
```

## Serve latest artifacts

Start a small Flask server that exposes `/latest`:

```bash
python src/server.py
```

Then open `http://localhost:5000/latest` to fetch the latest clean data, summary, and anomalies as JSON.

## Data layout

- `data/raw/` — raw CoinGecko JSON: `bitcoin_YYYY-MM-DD.json`
- `data/clean/` — cleaned daily snapshots: `bitcoin_clean_YYYY-MM-DD.json`
- `data/anomalies.json` — current anomalies array
- `data/summary/` — AI text summaries: `summary_YYYY-MM-DD.txt`
- `data/report/` — generated HTML reports: `report_YYYY-MM-DD.html`

## Environment & secrets

- The repository uses `python-dotenv` to load env variables from `.env` during development.
- Required for AI summaries: `OPENAI_API_KEY`.
- Required for email: `EMAIL_FROM`, `EMAIL_PASSWORD`, `EMAIL_TO`, `SMTP_SERVER`, `SMTP_PORT`.

## Tests

- A `tests/` folder is present for future unit tests; running `pytest` will execute tests if added.

## Troubleshooting

- If the pipeline fails to fetch data, check `logs/fetch.log` for HTTP errors.
- If the AI summary fails, verify `OPENAI_API_KEY` and network access.
- If email fails, check SMTP settings and consider using an app password for secure providers.

## Next steps / Improvements

- Add a `requirements.txt` lockfile or `pyproject.toml` for reproducible installs. (A minimal `requirements.txt` was added.)
- Add unit tests for ETL and anomaly detection logic.
- Add CI workflow to run tests and optionally schedule the pipeline.
- Containerize the service with Docker for consistent deployment.

## License

This project doesn't include a license file. Add an appropriate `LICENSE` if you plan to publish or share publicly.

---


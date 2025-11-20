import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import os
import json
from dotenv import load_dotenv

load_dotenv()

EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_TO = os.getenv("EMAIL_TO")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = os.getenv("SMTP_PORT")


def send_daily_email(anomalies, clean_data, summary_text, report_path):
    """Send daily email with:
       - anomalies
       - clean data summary
       - AI summary
       - attached HTML report
    """

    today = datetime.now().strftime("%Y-%m-%d")

    # Subject changes based on anomalies
    if anomalies:
        subject = f"🚨 Bitcoin Daily Report — Anomalies Detected ({today})"
    else:
        subject = f"✅ Bitcoin Daily Report — No Anomalies ({today})"

    # ======================
    # Build email body
    # ======================
    body = f"📊 DAILY BITCOIN REPORT — {today}\n\n"

    body += "==============================\n"
    body += "🧠 AI Summary\n"
    body += "==============================\n"
    body += summary_text + "\n\n"

    body += "==============================\n"
    body += "🚨 Anomalies\n"
    body += "==============================\n"

    if anomalies:
        for a in anomalies:
            body += (
                f"- Metric: {a['metric']}\n"
                f"  Today: {a['today']}\n"
                f"  Yesterday: {a['yesterday']}\n"
                f"  Change: {a['change%']}%\n"
                f"  Note: {a['note']}\n\n"
            )
    else:
        body += "No anomalies detected today. All metrics look stable.\n\n"

    body += "==============================\n"
    body += "📈 Clean Data Snapshot\n"
    body += "==============================\n"
    body += json.dumps(clean_data, indent=2)

    # ======================
    # Build email object
    # ======================
    msg = MIMEMultipart()
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    # ======================
    # Attach HTML Report
    # ======================
    try:
        with open(report_path, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
            encoders.encode_base64(part)
            filename = os.path.basename(report_path)
            part.add_header("Content-Disposition", f"attachment; filename={filename}")
            msg.attach(part)
    except Exception as e:
        print("❌ Failed to attach report:", e)

    # ======================
    # SEND EMAIL
    # ======================
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_FROM, EMAIL_PASSWORD)
            server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())

        print("📧 Daily email sent successfully!")

    except Exception as e:
        print("❌ Failed to send email:", e)

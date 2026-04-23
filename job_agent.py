import requests
import sqlite3
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --------------------------
# DATABASE SETUP
# --------------------------
import os
conn = sqlite3.connect(os.path.expanduser("~/job_agent/jobs.db"))
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS jobs (
    id TEXT PRIMARY KEY
)
""")
conn.commit()

# --------------------------
# SEARCH FUNCTION
# --------------------------
def search_jobs():
    url = "https://serpapi.com/search.json"

    keywords = ["Service Transition Analyst", "Service Transition Manager"]
    locations = ["United Kingdom", "Luxembourg", "Canada"]

    all_jobs = []

    for keyword in keywords:
        for location in locations:
            params = {
                "engine": "google_jobs",
                "q": keyword,
                "location": location,
                "api_key": "3b043f7159f0b5870e3c77dc30e95c6bda64226d5a02f2abfa1e048a3cf44ab9"
            }

            response = requests.get(url, params=params)
            data = response.json()

            print(f"\nDEBUG: Keyword='{keyword}', Location='{location}'")
            print(data)  # Shows what the API returned

            jobs = data.get("jobs_results", [])
            all_jobs.extend(jobs)

    return all_jobs

# --------------------------
# EMAIL FUNCTION
# --------------------------
def send_email(jobs, to_email):
    if not jobs:
        print("No new jobs to send.")
        return

    # Email settings
    from_email = "jo.aziba@gmail.com"
    password = "sxssuclvfybcidtx"  # Use Gmail App Password

    # Compose message
    subject = f"New Job Listings ({len(jobs)})"
    body = ""

    for job in jobs:
        title = job.get("title", "No Title")
        company = job.get("company_name", "No Company")
        location = job.get("location", "No Location")
        link = job.get("source_link", "No Link")
        body += f"{title} - {company} ({location})\nApply here: {link}\n\n"

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Send email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)
        server.send_message(msg)
        server.quit()
        print(f"Email sent to {to_email} ✅")
    except Exception as e:
        print("Error sending email:", e)

# --------------------------
# MAIN SCRIPT
# --------------------------
if __name__ == "__main__":
    print("Job agent started at:", datetime.now())

    jobs = search_jobs()
    print(f"\nTotal new jobs found: {len(jobs)}\n")

    for job in jobs:
        title = job.get("title", "No Title")
        company = job.get("company_name", "No Company")
        location = job.get("location", "No Location")
        link = job.get("source_link", "No Link")

        print(f"{title} - {company} ({location})")
        print(f"Apply here: {link}\n")

    # Send results to your email
    send_email(jobs, "jo.aziba@gmail.com")
    print("Job agent finished at:", datetime.now())

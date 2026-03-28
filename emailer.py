import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import EMAIL_USER, EMAIL_PASS, RECEIVER_EMAIL
from utils import logger

def send_email(html_body, lead_count=0, date_str=""):
    subject = f"Daily CAC Businesses Without Websites – {date_str} ({lead_count} Leads)"
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = EMAIL_USER
    msg["To"] = RECEIVER_EMAIL
    msg.attach(MIMEText(html_body, "html"))
    try:
        with smtplib.SMTP("smtp-relay.brevo.com", 587) as server:
            server.ehlo()
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.sendmail(EMAIL_USER, RECEIVER_EMAIL, msg.as_string())
        logger.info(f"Email sent to {RECEIVER_EMAIL}")
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        raise

import os
import resend

RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL", "jobhauntgithub@gmail.com")
EMAIL_FROM = "CAC Lead Bot <onboarding@resend.dev>"

resend.api_key = os.getenv("RESEND_API_KEY")


def send_email(html_body, lead_count=0, date_str=""):
    subject = f"Daily CAC Businesses Without Websites – {date_str} ({lead_count} Leads)"

    try:
        params = {
            "from": EMAIL_FROM,
            "to": [RECEIVER_EMAIL],
            "subject": subject,
            "html": html_body,
        }
        email = resend.Emails.send(params)
        print(f"[INFO] Email sent successfully. ID: {email['id']}")
    except Exception as e:
        print(f"[ERROR] Failed to send email: {e}")
        raise

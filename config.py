import os

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL", "jobhauntgithub@gmail.com")

LOCATION = "Lagos"
COUNTRY = "Nigeria"

EXCLUDED_DOMAINS = [
    "facebook.com", "instagram.com", "twitter.com", "x.com",
    "linkedin.com", "tiktok.com", "youtube.com",
    "vconnect.com", "yellowpages.com.ng", "businesslist.com.ng",
    "whogohost.com", "ngcareers.com", "jobberman.com",
    "trovit.com.ng", "nigeriabusinessdirectory.com",
    "infobel.com", "cylex.com.ng", "hotfrog.com.ng"
]

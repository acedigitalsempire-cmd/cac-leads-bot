import requests
import time
from config import GOOGLE_API_KEY, SEARCH_ENGINE_ID, EXCLUDED_DOMAINS
from utils import logger

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; CACLeadBot/1.0)"}

def is_excluded_domain(url):
    url_lower = url.lower()
    return any(domain in url_lower for domain in EXCLUDED_DOMAINS)

def search_business_online(business_name, retries=3):
    query = f'{business_name} Lagos Nigeria official website'
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": GOOGLE_API_KEY,
        "cx": SEARCH_ENGINE_ID,
        "q": query,
        "num": 5,
        "gl": "ng",
        "hl": "en"
    }
    for attempt in range(retries):
        try:
            res = requests.get(url, params=params, timeout=15)
            if res.status_code == 429:
                logger.warning("Rate limit hit — waiting 30s")
                time.sleep(30)
                continue
            if res.status_code != 200:
                return []
            data = res.json()
            return [item.get("link", "") for item in data.get("items", [])]
        except Exception as e:
            logger.error(f"Search error (attempt {attempt+1}): {e}")
            time.sleep(5)
    return []

def validate_website(url):
    if not url or not url.startswith("http"):
        return False
    try:
        res = requests.get(url, timeout=10, headers=HEADERS, allow_redirects=True)
        return res.status_code == 200 and len(res.text) > 1000
    except Exception:
        return False

def check_website(business_name):
    links = search_business_online(business_name)
    time.sleep(1)
    real_links = [l for l in links if not is_excluded_domain(l)]

    if not real_links:
        return {
            "has_website": False,
            "website_status": "No Website Found",
            "website_url": "",
            "confidence": "High"
        }

    top_link = real_links[0]
    if validate_website(top_link):
        return {
            "has_website": True,
            "website_status": "Has Website",
            "website_url": top_link,
            "confidence": "High"
        }

    return {
        "has_website": False,
        "website_status": "Broken Website",
        "website_url": top_link,
        "confidence": "Medium"
    }

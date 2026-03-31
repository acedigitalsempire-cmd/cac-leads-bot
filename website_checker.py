import requests
import time
from config import GOOGLE_API_KEY, SEARCH_ENGINE_ID, EXCLUDED_DOMAINS
from utils import logger

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; CACLeadBot/1.0)"}


def is_excluded_domain(url):
    url_lower = url.lower()
    return any(domain in url_lower for domain in EXCLUDED_DOMAINS)


def search_business_online(business_name, retries=3):
    """Run 2 different search queries to be more thorough"""
    queries = [
        f'"{business_name}" Nigeria official website',
        f'{business_name} Lagos Nigeria site',
    ]

    all_links = []
    for query in queries:
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
                    logger.warning("Rate limit hit — waiting 60s")
                    time.sleep(60)
                    continue
                if res.status_code != 200:
                    break
                data = res.json()
                links = [item.get("link", "") for item in data.get("items", [])]
                all_links += links
                break
            except Exception as e:
                logger.error(f"Search error (attempt {attempt+1}): {e}")
                time.sleep(5)
        time.sleep(2)

    return list(set(all_links))


def validate_website(url):
    """Strictly validate that a URL is a real working business website"""
    if not url or not url.startswith("http"):
        return False
    try:
        res = requests.get(url, timeout=10, headers=HEADERS, allow_redirects=True)
        # Must return 200 and have substantial content
        if res.status_code == 200 and len(res.text) > 2000:
            return True
        return False
    except Exception:
        return False


def check_website(business_name):
    """
    Stricter check — only marks as NO WEBSITE if:
    - Zero real links found across 2 searches AND
    - No working domain validated
    """
    links = search_business_online(business_name)
    time.sleep(2)

    # Filter out social media and directories
    real_links = [l for l in links if not is_excluded_domain(l)]

    if not real_links:
        return {
            "has_website": False,
            "website_status": "No Website Found",
            "website_url": "",
            "confidence": "High"  # High confidence — nothing found anywhere
        }

    # Check each real link strictly
    working_sites = []
    for link in real_links[:3]:  # Check top 3 real links
        if validate_website(link):
            working_sites.append(link)

    if working_sites:
        return {
            "has_website": True,
            "website_status": "Has Website",
            "website_url": working_sites[0],
            "confidence": "High"
        }

    # Links found but none working = broken website
    return {
        "has_website": False,
        "website_status": "Broken Website",
        "website_url": real_links[0] if real_links else "",
        "confidence": "Medium"  # Medium — links existed but were broken
    }

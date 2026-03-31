import requests
from bs4 import BeautifulSoup
from utils import logger, rate_limit, clean_text

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def fetch_businesslist():
    businesses = []
    for page in range(1, 4):
        url = f"https://www.businesslist.com.ng/location/lagos/{page}"
        try:
            res = requests.get(url, headers=HEADERS, timeout=30)
            if res.status_code != 200:
                logger.warning(f"[BusinessList] Page {page} status: {res.status_code}")
                break
            soup = BeautifulSoup(res.text, "html.parser")
            cards = soup.select(".company")
            if not cards:
                cards = soup.select("h3.company-name, .listing h2, .biz-listing")
            if not cards:
                all_links = soup.select("a[href*='/company/']")
                for link in all_links:
                    name = clean_text(link.get_text())
                    if name and len(name) > 3:
                        businesses.append({
                            "name": name,
                            "type": "Enterprise",
                            "category": "General",
                            "contact": "N/A",
                            "location": "Lagos, Nigeria",
                            "source": "BusinessList.ng"
                        })
                logger.info(f"[BusinessList] Page {page}: {len(all_links)} found via links")
                rate_limit(3)
                continue
            for card in cards:
                name_el = card.select_one("h3, h2, .name")
                phone_el = card.select_one(".phone, .tel")
                cat_el = card.select_one(".category, .cat")
                name = clean_text(name_el.get_text()) if name_el else None
                if not name:
                    continue
                businesses.append({
                    "name": name,
                    "type": "Enterprise",
                    "category": clean_text(cat_el.get_text()) if cat_el else "General",
                    "contact": clean_text(phone_el.get_text()) if phone_el else "N/A",
                    "location": "Lagos, Nigeria",
                    "source": "BusinessList.ng"
                })
            logger.info(f"[BusinessList] Page {page}: {len(cards)} found")
            rate_limit(3)
        except Exception as e:
            logger.error(f"[BusinessList] Error: {e}")
            break
    return businesses


def fetch_compass():
    """Fetch from Kompass Nigeria business directory"""
    businesses = []
    url = "https://ng.kompass.com/a/lagos-businesses/1/"
    try:
        res = requests.get(url, headers=HEADERS, timeout=30)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, "html.parser")
            cards = soup.select(".companyCard, .company-name, h2.title, .result-title")
            for card in cards:
                name = clean_text(card.get_text())
                if name and len(name) > 3:
                    businesses.append({
                        "name": name,
                        "type": "Enterprise",
                        "category": "General",
                        "contact": "N/A",
                        "location": "Lagos, Nigeria",
                        "source": "Kompass"
                    })
            logger.info(f"[Kompass] {len(businesses)} found")
        else:
            logger.warning(f"[Kompass] Status: {res.status_code}")
    except Exception as e:
        logger.error(f"[Kompass] Error: {e}")
    return businesses


def fetch_yellownpages():
    """Fetch from Nigerian Yellow Pages"""
    businesses = []
    pages = ["https://www.yellowpages.com.ng/Lagos",
             "https://www.yellowpages.com.ng/Lagos/Retail",
             "https://www.yellowpages.com.ng/Lagos/Services"]
    for url in pages:
        try:
            res = requests.get(url, headers=HEADERS, timeout=30)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, "html.parser")
                cards = soup.select(".business-name, .listing-name, h3, h2")
                for card in cards:
                    name = clean_text(card.get_text())
                    if name and len(name) > 3 and len(name) < 80:
                        businesses.append({
                            "name": name,
                            "type": "Enterprise",
                            "category": "General",
                            "contact": "N/A",
                            "location": "Lagos, Nigeria",
                            "source": "YellowPages.ng"
                        })
            logger.info(f"[YellowPages] {url}: {len(businesses)} found")
            rate_limit(3)
        except Exception as e:
            logger.error(f"[YellowPages] Error: {e}")
    return businesses


def fetch_all_businesses():
    logger.info("Starting business discovery...")
    all_businesses = []
    all_businesses += fetch_businesslist()
    all_businesses += fetch_compass()
    all_businesses += fetch_yellownpages()
    logger.info(f"Total collected: {len(all_businesses)}")
    return all_businesses

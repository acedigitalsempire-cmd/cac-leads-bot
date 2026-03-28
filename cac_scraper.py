import requests
from bs4 import BeautifulSoup
from utils import logger, rate_limit, clean_text

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 Chrome/91.0 Safari/537.36"
}

def fetch_businesslist():
    businesses = []
    for page in range(1, 4):
        url = f"https://www.businesslist.com.ng/location/lagos/{page}"
        try:
            res = requests.get(url, headers=HEADERS, timeout=20)
            if res.status_code != 200:
                break
            soup = BeautifulSoup(res.text, "html.parser")
            cards = soup.select(".company-list .company")
            if not cards:
                cards = soup.select(".listing, .business-item, article")
            for card in cards:
                name_el = card.select_one("h3, h2, .name, .title")
                phone_el = card.select_one(".phone, .tel, [class*='phone']")
                cat_el = card.select_one(".category, .cat, [class*='categ']")
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

def fetch_vconnect():
    businesses = []
    for page in range(1, 4):
        url = f"https://www.vconnect.com/find/businesses-in-Lagos?page={page}"
        try:
            res = requests.get(url, headers=HEADERS, timeout=20)
            if res.status_code != 200:
                break
            soup = BeautifulSoup(res.text, "html.parser")
            cards = soup.select(".business-card, .biz-item, .vendor-item, .listing-item")
            for card in cards:
                name_el = card.select_one("h2, h3, .biz-name, .vendor-name")
                phone_el = card.select_one(".phone, .contact-phone")
                cat_el = card.select_one(".category, .biz-category")
                name = clean_text(name_el.get_text()) if name_el else None
                if not name:
                    continue
                businesses.append({
                    "name": name,
                    "type": "Enterprise",
                    "category": clean_text(cat_el.get_text()) if cat_el else "General",
                    "contact": clean_text(phone_el.get_text()) if phone_el else "N/A",
                    "location": "Lagos, Nigeria",
                    "source": "VConnect"
                })
            logger.info(f"[VConnect] Page {page}: {len(cards)} found")
            rate_limit(3)
        except Exception as e:
            logger.error(f"[VConnect] Error: {e}")
            break
    return businesses

def fetch_nigeriangalleria():
    businesses = []
    url = "https://www.nigeriangalleria.com/Nigeria/States/Lagos/Business/"
    try:
        res = requests.get(url, headers=HEADERS, timeout=20)
        soup = BeautifulSoup(res.text, "html.parser")
        cards = soup.select("li, .business, .entry")
        for card in cards:
            name_el = card.select_one("a, h3, h4")
            name = clean_text(name_el.get_text()) if name_el else None
            if not name or len(name) < 3:
                continue
            businesses.append({
                "name": name,
                "type": "Enterprise",
                "category": "General",
                "contact": "N/A",
                "location": "Lagos, Nigeria",
                "source": "NigerianGalleria"
            })
        logger.info(f"[NigerianGalleria] {len(businesses)} found")
    except Exception as e:
        logger.error(f"[NigerianGalleria] Error: {e}")
    return businesses

def fetch_all_businesses():
    logger.info("Starting business discovery...")
    all_businesses = []
    all_businesses += fetch_businesslist()
    all_businesses += fetch_vconnect()
    all_businesses += fetch_nigeriangalleria()
    logger.info(f"Total collected: {len(all_businesses)}")
    return all_businesses

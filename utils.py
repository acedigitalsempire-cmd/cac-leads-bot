import time
import logging

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

def deduplicate(businesses):
    seen = set()
    unique = []
    for biz in businesses:
        key = biz.get("name", "").lower().strip()
        if key and key not in seen:
            seen.add(key)
            unique.append(biz)
    logger.info(f"Deduplicated to {len(unique)} unique businesses")
    return unique

def rate_limit(seconds=3):
    time.sleep(seconds)

def clean_text(text):
    if not text:
        return "N/A"
    return " ".join(text.strip().split())

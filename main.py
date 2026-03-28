from cac_scraper import fetch_all_businesses
from website_checker import check_website
from emailer import send_email
from utils import deduplicate, logger, rate_limit
from datetime import datetime

MAX_BUSINESSES = 50

def generate_html(leads, date_str):
    if not leads:
        return f"""
        <html><body style="font-family:Arial,sans-serif;background:#f4f4f4;padding:20px;">
        <div style="max-width:600px;margin:auto;background:white;border-radius:10px;padding:30px;text-align:center;">
        <h2 style="color:#e74c3c;">No Leads Found Today</h2>
        <p style="color:#555;">All businesses checked today appear to have functional websites.</p>
        <p style="color:#888;font-size:12px;">Date: {date_str}</p>
        </div></body></html>
        """
    rows = ""
    for i, biz in enumerate(leads):
        bg = "#ffffff" if i % 2 == 0 else "#f9f9f9"
        status = biz.get("website_status", "No Website Found")
        status_color = "#e74c3c" if status == "No Website Found" else "#e67e22"
        rows += f"""
        <tr style="background:{bg};">
        <td style="padding:12px;border-bottom:1px solid #eee;"><strong>{biz['name']}</strong></td>
        <td style="padding:12px;border-bottom:1px solid #eee;">{biz.get('type','Enterprise')}</td>
        <td style="padding:12px;border-bottom:1px solid #eee;">{biz.get('category','General')}</td>
        <td style="padding:12px;border-bottom:1px solid #eee;">{biz.get('contact','N/A')}</td>
        <td style="padding:12px;border-bottom:1px solid #eee;">{biz.get('location','Lagos, Nigeria')}</td>
        <td style="padding:12px;border-bottom:1px solid #eee;">
        <span style="background:{status_color};color:white;padding:4px 10px;border-radius:10px;font-size:12px;">{status}</span>
        </td>
        <td style="padding:12px;border-bottom:1px solid #eee;font-size:11px;">{biz.get('source','N/A')}</td>
        </tr>"""

    no_website = sum(1 for b in leads if b.get("website_status") == "No Website Found")
    broken = sum(1 for b in leads if b.get("website_status") == "Broken Website")

    return f"""
    <html><body style="font-family:Arial,sans-serif;background:#f4f4f4;padding:20px;margin:0;">
    <div style="max-width:1100px;margin:auto;background:white;border-radius:12px;overflow:hidden;box-shadow:0 4px 15px rgba(0,0,0,0.1);">
    <div style="background:linear-gradient(135deg,#1a1a2e,#16213e);padding:30px;text-align:center;">
    <h1 style="color:#f1c40f;margin:0;font-size:24px;">🏢 CAC Business Leads Report</h1>
    <p style="color:#aaa;margin:8px 0 0;">{date_str} — Lagos, Nigeria</p>
    <p style="color:white;font-size:18px;margin:10px 0 4px;"><strong>{len(leads)}</strong> Businesses Without Functional Websites</p>
    <p style="color:#ccc;font-size:13px;margin:0;">🔴 No Website: <strong>{no_website}</strong> &nbsp;|&nbsp; 🟠 Broken: <strong>{broken}</strong></p>
    </div>
    <div style="padding:20px;overflow-x:auto;">
    <table style="width:100%;border-collapse:collapse;font-size:14px;">
    <thead><tr style="background:#2c3e50;color:white;">
    <th style="padding:12px;text-align:left;">Business Name</th>
    <th style="padding:12px;text-align:left;">Type</th>
    <th style="padding:12px;text-align:left;">Category</th>
    <th style="padding:12px;text-align:left;">Contact</th>
    <th style="padding:12px;text-align:left;">Location</th>
    <th style="padding:12px;text-align:left;">Website Status</th>
    <th style="padding:12px;text-align:left;">Source</th>
    </tr></thead>
    <tbody>{rows}</tbody>
    </table></div>
    <div style="background:#f8f8f8;padding:20px;text-align:center;border-top:1px solid #eee;">
    <p style="color:#aaa;font-size:12px;margin:0;">
    💡 These businesses have no functional website — perfect prospects for your digital marketing services!<br>
    Generated automatically by your CAC Lead Bot 🤖 — runs daily at 10AM Nigeria Time.
    </p></div></div></body></html>"""

def main():
    date_str = datetime.now().strftime("%A, %B %d, %Y")
    logger.info(f"Starting CAC Lead Bot — {date_str}")
    businesses = fetch_all_businesses()
    businesses = deduplicate(businesses)
    businesses = businesses[:MAX_BUSINESSES]
    logger.info(f"Checking {len(businesses)} businesses for websites...")
    leads = []
    for i, biz in enumerate(businesses):
        logger.info(f"[{i+1}/{len(businesses)}] Checking: {biz['name']}")
        result = check_website(biz["name"])
        rate_limit(3)
        if not result["has_website"]:
            biz["website_status"] = result["website_status"]
            biz["website_url"] = result["website_url"]
            leads.append(biz)
    logger.info(f"Found {len(leads)} businesses without websites")
    html = generate_html(leads, date_str)
    send_email(html, lead_count=len(leads), date_str=date_str)
    logger.info("Done!")

if __name__ == "__main__":
    main()

import re
import requests
from bs4 import BeautifulSoup
from typing import Dict, Any

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

def fetch_and_clean_website(url: str, timeout: int = 12) -> Dict[str, Any]:
    """
    Fetches raw HTML from a website, strips unnecessary scripts/styles,
    and extracts clean text + direct contact signals (mailto, tel, social links).
    """
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    try:
        response = requests.get(url, headers=DEFAULT_HEADERS, timeout=timeout)
        response.raise_for_status()
    except Exception as e:
        return {
            "success": False,
            "url": url,
            "error": str(e),
            "text": "",
            "raw_emails": [],
            "raw_phones": [],
            "social_links": []
        }

    soup = BeautifulSoup(response.text, "html.parser")

    # 1. Extract direct mailto and tel links
    raw_emails = set()
    raw_phones = set()
    social_links = set()

    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if href.startswith("mailto:"):
            email = href.replace("mailto:", "").split("?")[0].strip()
            if email:
                raw_emails.add(email)
        elif href.startswith("tel:"):
            phone = href.replace("tel:", "").strip()
            if phone:
                raw_phones.add(phone)
        elif any(domain in href.lower() for domain in ["linkedin.com/company", "twitter.com", "x.com", "instagram.com", "facebook.com"]):
            social_links.add(href)

    # 2. Regex fallback for emails in raw HTML
    email_regex = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    found_emails = re.findall(email_regex, response.text)
    for em in found_emails:
        if not any(em.endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".webp", ".svg", ".js"]):
            raw_emails.add(em)

    # 3. Strip non-content tags
    for tag in soup(["script", "style", "noscript", "svg", "header", "footer", "nav", "iframe"]):
        tag.decompose()

    # 4. Extract and clean visible text
    text = soup.get_text(separator=" ", strip=True)
    text = re.sub(r'\s+', ' ', text)
    trimmed_text = text[:12000]

    return {
        "success": True,
        "url": url,
        "error": None,
        "text": trimmed_text,
        "raw_emails": list(raw_emails)[:5],
        "raw_phones": list(raw_phones)[:3],
        "social_links": list(social_links)[:5]
    }

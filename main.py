import os
import sys
import csv
import argparse
from datetime import datetime
from dotenv import load_dotenv

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from scraper import fetch_and_clean_website
from ai_extractor import extract_lead_info

load_dotenv()

CSV_FILENAME = "leads_output.csv"
CSV_FIELDS = [
    "Timestamp",
    "Source URL",
    "Company Name",
    "Industry",
    "Tagline / Pitch",
    "Target Audience",
    "Key Offerings",
    "Contact Email",
    "Contact Phone",
    "Location / HQ",
    "Social Profile"
]

def init_csv():
    if not os.path.exists(CSV_FILENAME):
        with open(CSV_FILENAME, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
            writer.writeheader()

def save_to_csv(url: str, lead: dict):
    init_csv()
    with open(CSV_FILENAME, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        offerings = ", ".join(lead.get("key_offerings", []))
        writer.writerow({
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Source URL": url,
            "Company Name": lead.get("company_name", "N/A"),
            "Industry": lead.get("industry", "N/A"),
            "Tagline / Pitch": lead.get("tagline_or_pitch", "N/A"),
            "Target Audience": lead.get("target_audience", "N/A"),
            "Key Offerings": offerings,
            "Contact Email": lead.get("contact_email") or "Not found",
            "Contact Phone": lead.get("contact_phone") or "Not found",
            "Location / HQ": lead.get("location_or_hq") or "Not found",
            "Social Profile": lead.get("primary_social") or "Not found"
        })

def print_banner():
    print("=" * 65)
    print("      AI LEAD & BUSINESS INTELLIGENCE SCRAPER")
    print("      Powered by Python + Google Gemini AI")
    print("=" * 65)

def print_lead_summary(url: str, lead: dict):
    print("\n" + "-" * 65)
    print(f" [SUCCESS] Extracted Profile: {lead.get('company_name', 'Unknown')}")
    print("-" * 65)
    print(f"  * URL:             {url}")
    print(f"  * Industry:        {lead.get('industry', 'N/A')}")
    print(f"  * Pitch:           {lead.get('tagline_or_pitch', 'N/A')}")
    print(f"  * Target Market:   {lead.get('target_audience', 'N/A')}")
    print(f"  * Offerings:       {', '.join(lead.get('key_offerings', []))}")
    print(f"  * Email:           {lead.get('contact_email') or 'N/A'}")
    print(f"  * Phone:           {lead.get('contact_phone') or 'N/A'}")
    print(f"  * HQ / Location:   {lead.get('location_or_hq') or 'N/A'}")
    print(f"  * Social:          {lead.get('primary_social') or 'N/A'}")
    print("-" * 65)

def process_url(url: str):
    url = url.strip().lstrip("\ufeff")
    if not url:
        return
    print(f"\n[1/2] Scraping: {url} ...")
    scraped = fetch_and_clean_website(url)

    if not scraped["success"]:
        print(f" [!] Failed to scrape {url}: {scraped['error']}")
        return

    print("[2/2] Analyzing content with Gemini AI...")
    result = extract_lead_info(
        url=url,
        webpage_text=scraped["text"],
        raw_emails=scraped["raw_emails"],
        raw_phones=scraped["raw_phones"],
        social_links=scraped["social_links"]
    )

    if not result["success"]:
        print(f" [!] AI Extraction Error: {result['error']}")
        return

    lead = result["lead"]
    print_lead_summary(url, lead)
    save_to_csv(url, lead)
    print(f" [OK] Saved cleanly to {CSV_FILENAME}")

def main():
    print_banner()

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("\n[!] Error: GEMINI_API_KEY is not set.")
        sys.exit(1)

    parser = argparse.ArgumentParser(description="AI Lead Scraper CLI")
    parser.add_argument("--url", help="Single website URL to scrape and analyze")
    parser.add_argument("--file", help="Path to text file containing URLs")

    args = parser.parse_args()

    if args.url:
        process_url(args.url)
    elif args.file:
        if not os.path.exists(args.file):
            print(f"File not found: {args.file}")
            sys.exit(1)
        with open(args.file, "r", encoding="utf-8") as f:
            urls = [line.strip().lstrip("\ufeff") for line in f if line.strip() and not line.startswith("#")]
        print(f"Found {len(urls)} URLs to process.")
        for u in urls:
            process_url(u)
    else:
        print("\nSelect an option:")
        print(" 1. Analyze a single website URL")
        print(" 2. Batch analyze websites from 'urls.txt'")
        print(" 3. Exit")
        choice = input("\nEnter choice (1/2/3 or paste URL): ").strip()

        if choice == "1":
            target = input("Enter website URL (e.g. stripe.com): ").strip()
            if target:
                process_url(target)
        elif choice == "2":
            file_path = "urls.txt"
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    urls = [line.strip().lstrip("\ufeff") for line in f if line.strip() and not line.startswith("#")]
                for u in urls:
                    process_url(u)
        else:
            print("Goodbye!")

if __name__ == "__main__":
    main()

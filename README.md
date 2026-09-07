# AI-Powered Lead & Business Intelligence Scraper 🚀

An automated Python tool that extracts, enriches, and structures company profile data from raw websites using **BeautifulSoup** and **Google Gemini AI**.

Outputs clean, normalized B2B data directly into a spreadsheet-ready **CSV / Google Sheet format**.

---

## 🌟 Key Features

- **Automated Web Sanitization:** Extracts clean content while filtering out boilerplate scripts, ads, and noisy DOM tags.
- **Direct Signal Detection:** Detects `mailto:` emails, `tel:` phone numbers, and company social profiles (LinkedIn, X, Instagram) from raw HTML.
- **LLM Structured Extraction:** Leverages **Gemini 2.5 Flash** with Pydantic JSON schemas to reliably output:
  - Company Legal / Trading Name
  - 1-2 sentence core value proposition & pitch
  - Primary industry & target market
  - Key products / services offered
  - Direct contact email and phone
  - Global / regional headquarters location
- **Batch Processing:** Scrape a single URL or an entire list from `urls.txt`.
- **CSV Export:** Automatically appends structured rows to `leads_output.csv`.

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **Google GenAI SDK** (`google-genai` / Gemini 2.5 Flash)
- **Pydantic v2** (Type validation & strict schema enforcement)
- **BeautifulSoup4 & Requests** (HTML parsing & web scraping)
- **Python-Dotenv** (Environment variable management)

---

## 🚀 Quickstart Guide

### 1. Clone & Install Dependencies

```bash
git clone https://github.com/your-username/ai-lead-scraper.git
cd ai-lead-scraper
pip install -r requirements.txt
```

### 2. Configure API Key

1. Get a free Google Gemini API key at [Google AI Studio](https://aistudio.google.com/app/apikey).
2. Create a `.env` file in the project root:
```env
GEMINI_API_KEY=your_actual_api_key_here
```

### 3. Run the Tool

**Single URL Mode:**
```bash
py main.py --url https://stripe.com
```

**Batch Processing Mode:**
```bash
py main.py --file urls.txt
```

**Interactive Menu:**
```bash
py main.py
```

---

## 📊 Sample Output (`leads_output.csv`)

| Timestamp | Company Name | Industry | Tagline / Pitch | Target Audience | Contact Email | Social Profile |
|-----------|--------------|----------|-----------------|-----------------|---------------|----------------|
| 2026-09-06 14:30 | Stripe | FinTech / Payments | Financial infrastructure for the internet. | Startups to Enterprises | info@stripe.com | https://linkedin.com/company/stripe |

---

## 💼 Commercial Use Cases

- **B2B Sales Prospecting:** Auto-enrich leads before outreach campaigns.
- **Competitor Market Research:** Extract core features and positioning across 50+ competitors in minutes.
- **Directory Scraping:** Convert raw web directories into structured client databases.

---

## 📄 License
MIT License. Free for commercial and personal use.

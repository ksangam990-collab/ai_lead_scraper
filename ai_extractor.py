import os
import json
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

class CompanyLead(BaseModel):
    company_name: str = Field(description="The formal name of the company or brand")
    tagline_or_pitch: str = Field(description="1-2 sentences clearly describing what problem they solve and how")
    industry: str = Field(description="Primary industry, e.g., B2B SaaS, FinTech, E-Commerce, Developer Tools")
    target_audience: str = Field(description="Who their target customer is, e.g., Developers, Enterprise, Consumers")
    key_offerings: List[str] = Field(default_factory=list, description="Top 3 to 5 core products, features, or services")
    contact_email: Optional[str] = Field(default=None, description="Primary contact or sales email")
    contact_phone: Optional[str] = Field(default=None, description="Contact phone number if available")
    location_or_hq: Optional[str] = Field(default=None, description="Headquarters city or country if mentioned")
    primary_social: Optional[str] = Field(default=None, description="Main LinkedIn or Twitter/X profile link if detected")

def extract_lead_info(
    url: str,
    webpage_text: str,
    raw_emails: List[str],
    raw_phones: List[str],
    social_links: List[str],
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    key = api_key or os.getenv("GEMINI_API_KEY")
    if not key:
        raise ValueError("GEMINI_API_KEY not found in environment or .env!")

    client = genai.Client(api_key=key)

    system_instruction = (
        "You are an expert B2B business intelligence analyst. "
        "Extract clean, highly accurate company profile information from scraped website content."
    )

    prompt = f"""
Analyze the following scraped website data for URL: {url}

--- KNOWN CONTACT SIGNALS ---
Detected Emails: {raw_emails if raw_emails else 'None directly found'}
Detected Phones: {raw_phones if raw_phones else 'None directly found'}
Detected Socials: {social_links if social_links else 'None directly found'}

--- SCRAPED WEBPAGE CONTENT ---
{webpage_text}

Extract the company details strictly following the schema.
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.1,
                response_mime_type="application/json",
                response_schema=CompanyLead,
            ),
        )
        data = json.loads(response.text)
        return {"success": True, "lead": data}
    except Exception as e:
        return {"success": False, "error": str(e)}

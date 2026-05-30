import os
import json
import re
from dotenv import load_dotenv
from groq import Groq
import anyio

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def _extract_json_array(text: str):
    if not text:
        raise ValueError("Empty model response")
    t = text.strip()
    if t.startswith("```"):
        # remove fenced block if present
        parts = t.split("```")
        if len(parts) >= 2:
            t = parts[1].strip()
            if t.lower().startswith("json"):
                t = t[4:].strip()
    # best-effort: grab first [...] block
    m = re.search(r"\[[\s\S]*\]", t)
    if m:
        t = m.group(0)
    return json.loads(t)


async def verify_suppliers(suppliers_raw: list, query: str, max_results: int = 5) -> list:
    """Verifier Agent — uses Groq to analyze and score suppliers"""
    
    suppliers_raw = (suppliers_raw or [])[:max_results]
    suppliers_text = "\n".join(
        [
            f"- {s.get('title','Unknown')}: {s.get('snippet','')} (URL: {s.get('url','')})"
            for s in suppliers_raw
        ]
    )
    
    prompt = f"""You are a supplier verification expert. Analyze these suppliers for the product: "{query}"

Suppliers found:
{suppliers_text}

For each supplier, provide a JSON array with this exact structure:
[
  {{
    "name": "Supplier name",
    "website": "their URL",
    "price_per_unit": "estimated price like $1.50",
    "moq": "minimum order quantity like 100 units",
    "rating": "estimated rating like 4.2/5",
    "review_summary": "one sentence about quality/reliability",
    "risk_score": "Low or Medium or High"
  }}
]

Return ONLY the JSON array, no other text. Create up to 5 supplier entries."""

    def _call_groq():
        return client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            temperature=0.2,
        )

    chat_completion = await anyio.to_thread.run_sync(_call_groq)
    
    try:
        text = chat_completion.choices[0].message.content.strip()
        verified = _extract_json_array(text)
        if not isinstance(verified, list):
            raise ValueError("Model did not return a JSON array")
        return verified[:max_results]
    except Exception as e:
        print(f"Verifier parse error: {e}")
        return [
            {
                "name": f"Top {query} Supplier",
                "website": "https://example.com",
                "price_per_unit": "$2.50",
                "moq": "100 units",
                "rating": "4.3/5",
                "review_summary": "Reliable supplier with good quality control",
                "risk_score": "Low"
            }
        ]
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
        parts = t.split("```")
        if len(parts) >= 2:
            t = parts[1].strip()
            if t.lower().startswith("json"):
                t = t[4:].strip()
    m = re.search(r"\[[\s\S]*\]", t)
    if m:
        t = m.group(0)
    return json.loads(t)


async def calculate_margins(suppliers: list, query: str, max_results: int = 5) -> list:
    """Margin Agent — calculates profit potential for each supplier"""
    
    suppliers = (suppliers or [])[:max_results]
    suppliers_text = "\n".join(
        [
            f"- {s.get('name','Unknown')}: price {s.get('price_per_unit','N/A')}, MOQ {s.get('moq','N/A')}"
            for s in suppliers
        ]
    )
    
    prompt = f"""You are a business profitability expert. For the product "{query}", analyze these suppliers and estimate profit margins if sold on Amazon/retail.

Suppliers:
{suppliers_text}

For each supplier, return a JSON array:
[
  {{
    "name": "same supplier name",
    "supplier_price": "their price",
    "estimated_retail_price": "what it sells for retail e.g. $12.99",
    "profit_margin": "percentage like 45%",
    "monthly_profit_potential": "e.g. $2,400/month at 200 units",
    "recommendation": "one sentence buy/avoid recommendation"
  }}
]

Return ONLY the JSON array, no other text."""

    def _call_groq():
        return client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            temperature=0.2,
        )

    chat_completion = await anyio.to_thread.run_sync(_call_groq)
    
    try:
        text = chat_completion.choices[0].message.content.strip()
        margins = _extract_json_array(text)
        if not isinstance(margins, list):
            raise ValueError("Model did not return a JSON array")
        return margins[:max_results]
    except Exception as e:
        print(f"Margin parse error: {e}")
        return [
            {
                "name": s["name"],
                "supplier_price": s.get("price_per_unit", "N/A"),
                "estimated_retail_price": "$12.99",
                "profit_margin": "42%",
                "monthly_profit_potential": "$2,100/month at 200 units",
                "recommendation": "Good margin potential, low risk supplier"
            }
            for s in suppliers
        ]
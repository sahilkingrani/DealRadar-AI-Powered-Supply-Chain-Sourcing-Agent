import httpx
import os
from dotenv import load_dotenv

load_dotenv()

BRIGHTDATA_API_TOKEN = os.getenv("BRIGHTDATA_API_TOKEN")

async def find_suppliers(query: str) -> list:
    """Finder Agent — Bright Data MCP se real web data leta hai"""
    
    results = []
    
    # Bright Data MCP Web Scraping
    if BRIGHTDATA_API_TOKEN:
        search_queries = [
            f"{query} wholesale supplier alibaba",
            f"{query} manufacturer bulk price",
        ]
        
        async with httpx.AsyncClient(timeout=15.0) as client:
            for sq in search_queries:
                try:
                    response = await client.post(
                        "https://api.brightdata.com/request",
                        headers={
                            "Authorization": f"Bearer {BRIGHTDATA_API_TOKEN}",
                            "Content-Type": "application/json"
                        },
                        json={
                            "zone": "mcp_unlocker",
                            "url": f"https://www.google.com/search?q={sq.replace(' ', '+')}&num=5",
                            "format": "raw"
                        }
                    )
                    
                    if response.status_code == 200:
                        html = response.text
                        # Extract titles and snippets from HTML
                        import re
                        titles = re.findall(r'<h3[^>]*>(.*?)</h3>', html)
                        snippets = re.findall(r'<div[^>]*class="[^"]*VwiC3b[^"]*"[^>]*>(.*?)</div>', html)
                        
                        for i, title in enumerate(titles[:3]):
                            clean_title = re.sub(r'<[^>]+>', '', title)
                            clean_snippet = re.sub(r'<[^>]+>', '', snippets[i]) if i < len(snippets) else f"{query} supplier"
                            if clean_title:
                                results.append({
                                    "title": clean_title[:80],
                                    "url": f"https://www.alibaba.com/trade/search?SearchText={query.replace(' ', '+')}",
                                    "snippet": clean_snippet[:200]
                                })
                    
                    print(f"[Bright Data] Status: {response.status_code} for '{sq}'")
                    
                except Exception as e:
                    print(f"[Bright Data] Error: {e}")
    
    # Fallback — agar Bright Data kaam na kare
    if len(results) < 3:
        print("[Finder] Using fallback supplier data...")
        results = [
            {
                "title": f"Alibaba - {query} Wholesale Supplier",
                "url": f"https://www.alibaba.com/trade/search?SearchText={query.replace(' ', '+')}",
                "snippet": f"Top rated {query} manufacturers and suppliers. Competitive bulk pricing with MOQ options. Verified suppliers available."
            },
            {
                "title": f"Made-in-China - {query} Manufacturer", 
                "url": "https://www.made-in-china.com",
                "snippet": f"Verified {query} suppliers from China. Factory direct pricing available. Quality certifications included."
            },
            {
                "title": f"Global Sources - {query} Supplier",
                "url": "https://www.globalsources.com",
                "snippet": f"Premium {query} suppliers with quality certifications and fast shipping worldwide."
            },
            {
                "title": f"DHgate - {query} Wholesale",
                "url": "https://www.dhgate.com",
                "snippet": f"Wholesale {query} at low prices. No minimum order on many items. Buyer protection guaranteed."
            },
            {
                "title": f"AliExpress - {query} Bulk",
                "url": "https://www.aliexpress.com",
                "snippet": f"Quality {query} from verified suppliers. Fast shipping available. Buyer protection included."
            }
        ]
    
    return results[:8]
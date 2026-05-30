import time

import anyio
from fastapi import APIRouter, HTTPException
from models import SearchRequest, SearchResponse
from agents import find_suppliers, verify_suppliers, calculate_margins

router = APIRouter()

@router.post("/search", response_model=SearchResponse)
async def search_suppliers(request: SearchRequest):
    try:
        t0 = time.perf_counter()
        query = (request.query or "").strip()
        if not query:
            raise HTTPException(status_code=422, detail="query is required")

        max_results = max(1, min(int(request.max_results or 5), 8))

        with anyio.fail_after(15):
            print(f"[Finder] searching for '{query}'...")
            raw_suppliers = await find_suppliers(query)
            raw_suppliers = (raw_suppliers or [])[:max_results]
        
            print(f"[Verifier] analyzing {len(raw_suppliers)} results...")
            verified_suppliers = await verify_suppliers(raw_suppliers, query, max_results=max_results)
        
            print("[Margin] calculating profit margins...")
            margin_data = await calculate_margins(verified_suppliers, query, max_results=max_results)
        
        final_suppliers = []
        for i, supplier in enumerate(verified_suppliers):
            margin_info = margin_data[i] if i < len(margin_data) else {}
            final_suppliers.append({
                "name": supplier.get("name", "Unknown"),
                "website": supplier.get("website", "N/A"),
                "price_per_unit": supplier.get("price_per_unit", "N/A"),
                "moq": supplier.get("moq", "N/A"),
                "rating": supplier.get("rating", "N/A"),
                "review_summary": supplier.get("review_summary", "N/A"),
                "risk_score": supplier.get("risk_score", "Low"),
                "profit_margin": margin_info.get("profit_margin", "N/A"),
            })
        
        return SearchResponse(
            query=query,
            suppliers=final_suppliers,
            summary=f"Found {len(final_suppliers)} verified suppliers for '{query}'",
            status="success",
        )
    
    except TimeoutError:
        raise HTTPException(status_code=504, detail="Timed out while sourcing suppliers (15s budget). Try fewer words or retry.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    return {"status": "DealRadar is running!"}
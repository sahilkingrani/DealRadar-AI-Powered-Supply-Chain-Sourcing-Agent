from pydantic import BaseModel
from typing import List, Optional

class SearchRequest(BaseModel):
    query: str
    max_results: int = 5

class Supplier(BaseModel):
    name: str
    website: str
    price_per_unit: Optional[str] = "N/A"
    moq: Optional[str] = "N/A"
    rating: Optional[str] = "N/A"
    review_summary: Optional[str] = "N/A"
    risk_score: Optional[str] = "Low"
    profit_margin: Optional[str] = "N/A"

class SearchResponse(BaseModel):
    query: str
    suppliers: List[Supplier]
    summary: str
    status: str
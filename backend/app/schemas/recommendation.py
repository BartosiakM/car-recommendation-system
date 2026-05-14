from pydantic import BaseModel
from typing import Optional

class RecommendationOut(BaseModel):
    vehicle_id: int
    vehicle_name: str

    performance_score: float
    size_score: float
    economy_score: float
    practicality_score: float
    exoticness_score: float
    engagement_score: float

    match_percentage: int
    score: Optional[float] = None
    image_url: Optional[str] = None

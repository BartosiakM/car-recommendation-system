from pydantic import BaseModel
from typing import Optional

class AxesRatingUpsert(BaseModel):
    user_id: int
    vehicle_id: int

    performance: Optional[float] = None
    size: Optional[float] = None
    economy: Optional[float] = None
    practicality: Optional[float] = None
    exoticness: Optional[float] = None
    engagement: Optional[float] = None

class AxesRatingOut(BaseModel):
    id: int
    user_id: int
    vehicle_id: int
    vehicle_name: Optional[str] = None

    performance: Optional[float] = None
    size: Optional[float] = None
    economy: Optional[float] = None
    practicality: Optional[float] = None
    exoticness: Optional[float] = None
    engagement: Optional[float] = None

    class Config:
        from_attributes = True

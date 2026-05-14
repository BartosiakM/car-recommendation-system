from pydantic import BaseModel, Field
from typing import Optional

class VehicleOut(BaseModel):
    vehicle_id: int
    vehicle_name: Optional[str] = None
    production_year: Optional[float] = None

    performance_score: float
    size_score: float
    economy_score: float
    practicality_score: float
    exoticness_score: float
    engagement_score: float

    class Config:
        from_attributes = True


class VehicleCreate(BaseModel):
    vehicle_name: Optional[str] = None
    production_year: Optional[float] = None

    performance_score: float
    size_score: float
    economy_score: float
    practicality_score: float
    exoticness_score: float
    engagement_score: float


class VehicleUpdate(BaseModel):
    vehicle_name: Optional[str] = None
    production_year: Optional[float] = None

    performance_score: Optional[float] = None
    size_score: Optional[float] = None
    economy_score: Optional[float] = None
    practicality_score: Optional[float] = None
    exoticness_score: Optional[float] = None
    engagement_score: Optional[float] = None

class VehicleListItem(BaseModel):
    vehicle_id: int
    vehicle_name: Optional[str] = None

    class Config:
        from_attributes = True
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.recommendation import RecommendationOut
from app.utils.recommender import recommend

router = APIRouter(prefix="/recommendations", tags=["recommendations"])

@router.get("/user/{user_id}", response_model=List[RecommendationOut])
def recommendations(user_id: int, k: int = 10, rating_scale: str = "1_5", db: Session = Depends(get_db)):
    return recommend(db, user_id=user_id, k=k, rating_scale=rating_scale)

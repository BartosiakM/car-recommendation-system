from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy.orm import joinedload

from app.database import get_db
from app.models.vehicle import Vehicle
from app.models.user_vehicle_rating import UserVehicleRating
from app.schemas.ratings import AxesRatingUpsert, AxesRatingOut

router = APIRouter(prefix="/axes-ratings", tags=["axes-ratings"])

@router.post("/", response_model=AxesRatingOut)
def upsert_axes_rating(payload: AxesRatingUpsert, db: Session = Depends(get_db)):
    v = db.query(Vehicle).filter(Vehicle.vehicle_id == payload.vehicle_id).first()
    if not v:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    r = (
        db.query(UserVehicleRating)
        .filter(UserVehicleRating.user_id == payload.user_id,
                UserVehicleRating.vehicle_id == payload.vehicle_id)
        .first()
    )

    data = payload.model_dump(exclude_unset=True)

    if r:
        for k, val in data.items():
            if k in ("user_id", "vehicle_id"):
                continue
            setattr(r, k, val)
    else:
        r = UserVehicleRating(**data)
        db.add(r)

    db.commit()
    db.refresh(r)
    return r

@router.get("/user/{user_id}")
def list_user_axes_ratings(user_id: int, db: Session = Depends(get_db)):
    rows = (
        db.query(
            UserVehicleRating,
            Vehicle.vehicle_name
        )
        .join(Vehicle, Vehicle.vehicle_id == UserVehicleRating.vehicle_id)
        .filter(UserVehicleRating.user_id == user_id)
        .all()
    )

    return [
        {
            "id": r.UserVehicleRating.id,
            "user_id": r.UserVehicleRating.user_id,
            "vehicle_id": r.UserVehicleRating.vehicle_id,
            "vehicle_name": r.vehicle_name,
            "performance": r.UserVehicleRating.performance,
            "size": r.UserVehicleRating.size,
            "economy": r.UserVehicleRating.economy,
            "practicality": r.UserVehicleRating.practicality,
            "exoticness": r.UserVehicleRating.exoticness,
            "engagement": r.UserVehicleRating.engagement,
        }
        for r in rows
    ]
@router.delete("/user/{user_id}/vehicle/{vehicle_id}")
def delete_axes_rating(user_id: int, vehicle_id: int, db: Session = Depends(get_db)):
    r = (
        db.query(UserVehicleRating)
        .filter(UserVehicleRating.user_id == user_id,
                UserVehicleRating.vehicle_id == vehicle_id)
        .first()
    )
    if not r:
        raise HTTPException(status_code=404, detail="Rating not found")

    db.delete(r)
    db.commit()
    return {"status": "deleted"}

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import text

from app.database import get_db
from app.models.vehicle import Vehicle
from app.schemas.vehicle import VehicleOut, VehicleCreate, VehicleUpdate
from app.schemas.vehicle import VehicleListItem
from sqlalchemy import and_, case
router = APIRouter(prefix="/vehicles", tags=["vehicles"])


@router.get("/vehicle-options")
def vehicle_options(
    q: str = Query(min_length=2),
    limit: int = Query(default=20, ge=1, le=50),
    db: Session = Depends(get_db),
):
    query = q.strip()

    rows = db.execute(text("""
        SELECT vehicle_id, vehicle_name
        FROM vehicles
        WHERE to_tsvector('simple', coalesce(vehicle_name,'')) @@ plainto_tsquery('simple', :q)
        ORDER BY ts_rank(
          to_tsvector('simple', coalesce(vehicle_name,'')),
          plainto_tsquery('simple', :q)
        ) DESC
        LIMIT :limit
    """), {"q": query, "limit": limit}).all()

    return [{"vehicle_id": r[0], "vehicle_name": r[1]} for r in rows]

@router.get("/{vehicle_id}", response_model=VehicleOut)
def get_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    v = db.query(Vehicle).filter(Vehicle.vehicle_id == vehicle_id).first()
    if not v:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return v

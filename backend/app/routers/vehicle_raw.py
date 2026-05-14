from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.vehicle_raw import VehicleRaw

router = APIRouter(prefix="/vehicles", tags=["vehicles"])

@router.get("/{vehicle_id}/raw")
def get_vehicle_raw(vehicle_id: int, db: Session = Depends(get_db)):
    raw = db.query(VehicleRaw).filter(VehicleRaw.vehicle_id == vehicle_id).first()
    if not raw:
        raise HTTPException(status_code=404, detail="Vehicle raw not found")
    return raw.data

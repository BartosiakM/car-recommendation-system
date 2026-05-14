from pathlib import Path
import pandas as pd
from sqlalchemy.orm import Session

from app.models.vehicle import Vehicle
from app.models.vehicle_raw import VehicleRaw

def seed_if_empty(db: Session, core_csv: str, raw_csv: str) -> None:
    if db.query(Vehicle).first():
        return

    base_dir = Path(__file__).resolve().parents[2]
    core_path = base_dir / core_csv
    raw_path  = base_dir / raw_csv

    df_core = pd.read_csv(core_path)
    df_raw  = pd.read_csv(raw_path)

    core_records = df_core.to_dict(orient="records")
    db.bulk_insert_mappings(Vehicle, core_records)
    db.commit()

    raw_rows = []
    for row in df_raw.to_dict(orient="records"):
        vid = int(row["vehicle_id"])
        raw_rows.append({"vehicle_id": vid, "data": row})

    db.bulk_insert_mappings(VehicleRaw, raw_rows)
    db.commit()

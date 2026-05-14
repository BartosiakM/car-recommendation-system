from sqlalchemy import text
from app.database import engine, SessionLocal, Base
from app.db.seed import seed_if_empty

async def lifespan(app):
    Base.metadata.create_all(bind=engine)

    if engine.dialect.name == "postgresql":
        with engine.begin() as conn:
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS ix_vehicle_name_fts
                ON vehicles USING gin (to_tsvector('simple', coalesce(vehicle_name,'')));
            """))

    db = SessionLocal()
    try:
        seed_if_empty(db, "app/vehicles_features.csv", "app/vehicles_raw.csv")
    finally:
        db.close()

    yield

import os
import sys
from pathlib import Path
from contextlib import asynccontextmanager

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


@pytest.fixture(scope="session", autouse=True)
def _set_test_env():
    os.environ.setdefault("DATABASE_URL", "sqlite+pysqlite:///:memory:")


@pytest.fixture()
def _db_engine_and_sessionmaker():
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        future=True,
    )
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    return engine, TestingSessionLocal


@pytest.fixture()
def db_session(_db_engine_and_sessionmaker):
    """Sesja do seedowania danych w testach."""
    engine, TestingSessionLocal = _db_engine_and_sessionmaker

    from app.database import Base
    from app.models.vehicle import Vehicle
    from app.models.user_vehicle_rating import UserVehicleRating

    try:
        from app.models.user import User
        tables = [Vehicle.__table__, UserVehicleRating.__table__, User.__table__]
    except Exception:
        tables = [Vehicle.__table__, UserVehicleRating.__table__]

    Base.metadata.create_all(bind=engine, tables=tables)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(_db_engine_and_sessionmaker):
    engine, TestingSessionLocal = _db_engine_and_sessionmaker

    from app.database import Base, get_db
    from app.main import app

    from app.models.user import User
    Base.metadata.create_all(bind=engine, tables=[User.__table__])

    original_lifespan = app.router.lifespan_context

    @asynccontextmanager
    async def no_lifespan(_app):
        yield

    app.router.lifespan_context = no_lifespan

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as c:
            yield c
    finally:
        app.dependency_overrides.clear()
        app.router.lifespan_context = original_lifespan

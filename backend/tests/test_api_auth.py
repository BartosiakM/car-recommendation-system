import os
import pytest
from contextlib import asynccontextmanager
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool


@pytest.fixture(scope="session", autouse=True)
def _set_test_env():
    os.environ.setdefault("DATABASE_URL", "sqlite+pysqlite:///:memory:")


@pytest.fixture()
def client_and_db():
    from app.database import Base, get_db
    from app.main import app
    from app.models.user import User

    original_lifespan = app.router.lifespan_context

    @asynccontextmanager
    async def no_lifespan(_app):
        yield

    app.router.lifespan_context = no_lifespan

    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        future=True,
    )
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

    Base.metadata.create_all(bind=engine, tables=[User.__table__])

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as c:
            yield c, TestingSessionLocal
    finally:
        app.dependency_overrides.clear()
        app.router.lifespan_context = original_lifespan

def _register(client: TestClient, username: str, password: str):
    return client.post("/auth/register", json={"username": username, "password": password})


def _login(client: TestClient, username: str, password: str):
    return client.post("/auth/login", json={"username": username, "password": password})


def test_register_success_returns_userread(client_and_db):
    client, _ = client_and_db

    r = _register(client, "alice", "secret123")
    assert r.status_code == 201

    data = r.json()
    assert data["username"] == "alice"
    assert "user_id" in data
    assert "hashed_password" not in data


def test_register_conflict_when_username_exists(client_and_db):
    client, _ = client_and_db

    r1 = _register(client, "bob", "password123")
    assert r1.status_code == 201

    r2 = _register(client, "bob", "password123")
    assert r2.status_code == 409
    assert r2.json()["detail"] == "Użytkownik o takiej nazwie już istnieje"


def test_login_success_returns_token_and_user_id(client_and_db):
    client, _ = client_and_db

    _register(client, "carol", "password123")
    r = _login(client, "carol", "password123")
    assert r.status_code == 200

    data = r.json()
    assert data["token_type"] == "bearer"
    assert isinstance(data["access_token"], str) and len(data["access_token"]) > 10
    assert isinstance(data["user_id"], int)


def test_login_wrong_password_401_and_www_authenticate_header(client_and_db):
    client, _ = client_and_db

    _register(client, "dave", "password123")
    r = _login(client, "dave", "badpassword")
    assert r.status_code == 401
    assert r.json()["detail"] == "Nieprawidłowy login lub hasło"
    assert r.headers.get("WWW-Authenticate") == "Bearer"


def test_me_requires_auth_401(client_and_db):
    client, _ = client_and_db

    r = client.get("/auth/me")
    assert r.status_code in (401, 403)


def test_me_returns_current_user_when_token_valid(client_and_db):
    client, _ = client_and_db

    _register(client, "erin", "password123")
    login = _login(client, "erin", "password123")
    token = login.json()["access_token"]

    r = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200

    data = r.json()
    assert data["username"] == "erin"
    assert "user_id" in data

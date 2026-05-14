
def _register_and_login(client, username="jwt_user", password="haslo123"):

    r1 = client.post("/auth/register", json={"username": username, "password": password})
    assert r1.status_code in (201, 409), r1.text

    r2 = client.post("/auth/login", json={"username": username, "password": password})
    assert r2.status_code == 200, r2.text

    data = r2.json()
    assert "access_token" in data, r2.text
    return data["access_token"]


def test_me_requires_token(client):

    r = client.get("/auth/me")
    assert r.status_code in (401, 403), r.text


def test_me_with_invalid_token_returns_401(client):

    r = client.get("/auth/me", headers={"Authorization": "Bearer totally.fake.token"})
    assert r.status_code == 401, r.text


def test_me_with_valid_token_returns_user(client):

    token = _register_and_login(client, username="jwt_user_ok", password="haslo123")

    r = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200, r.text

    data = r.json()
    assert data["username"] == "jwt_user_ok"
    assert "user_id" in data
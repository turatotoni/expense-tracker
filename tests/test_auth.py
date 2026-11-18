def test_register(client):
    response = client.post(
        "/auth/register",
        json={"email": "ana@example.com", "password": "lozinka123"},
    )

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "ana@example.com"
    assert "id" in data
    assert "password_hash" not in data

def test_register_duplicate_email(client):
    payload = {"email": "ana@example.com", "password": "lozinka123"}

    client.post("/auth/register", json=payload)           # prvi put: prolazi
    response = client.post("/auth/register", json=payload)  # drugi put: duplikat

    assert response.status_code == 409

def test_register_short_password(client):
    response = client.post(
        "/auth/register",
        json={"email": "ana@example.com", "password": "kratka"},
    )

    assert response.status_code == 422

def test_login(client):
    client.post("/auth/register", json={"email": "ana@example.com", "password": "lozinka123"})

    response = client.post(
        "/auth/login",
        data={"username": "ana@example.com", "password": "lozinka123"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["token_type"] == "bearer"
    assert data["access_token"]


def test_login_wrong_password(client):
    client.post("/auth/register", json={"email": "ana@example.com", "password": "lozinka123"})

    response = client.post(
        "/auth/login",
        data={"username": "ana@example.com", "password": "kriva_lozinka"},
    )

    assert response.status_code == 401


def test_login_unknown_email(client):
    response = client.post(
        "/auth/login",
        data={"username": "nepoznat@example.com", "password": "lozinka123"},
    )

    assert response.status_code == 401

def test_me_requires_token(client):
    response = client.get("/auth/me")

    assert response.status_code == 401


def test_me(client, auth_headers):
    response = client.get("/auth/me", headers=auth_headers)

    assert response.status_code == 200
    assert response.json()["email"] == "ana@example.com"


def test_invalid_token_rejected(client):
    response = client.get("/auth/me", headers={"Authorization": "Bearer nesto.krivo.potpuno"})

    assert response.status_code == 401
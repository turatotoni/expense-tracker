def test_create_category(client, auth_headers):
    response = client.post("/categories", json={"name": "Hrana"}, headers=auth_headers)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Hrana"
    assert "id" in data

def test_create_duplicate_category(client, auth_headers):
    client.post("/categories", json={"name": "Hrana"}, headers=auth_headers)
    response = client.post("/categories", json={"name": "Hrana"}, headers=auth_headers)

    assert response.status_code == 409

def test_list_categories(client, auth_headers):
    client.post("/categories", json={"name": "Hrana"}, headers=auth_headers)
    client.post("/categories", json={"name": "Prijevoz"}, headers=auth_headers)

    response = client.get("/categories", headers=auth_headers)

    assert response.status_code == 200
    names = [c["name"] for c in response.json()]
    assert names == ["Hrana", "Prijevoz"]

def test_categories_require_auth(client):
    assert client.get("/categories").status_code == 401


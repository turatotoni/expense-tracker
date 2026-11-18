def create_category(client, headers, name="Hrana") -> int:
    response = client.post("/categories", json={"name": name}, headers=headers)
    return response.json()["id"]


def create_expense(client, headers, category_id, amount="45.30", spent_on="2026-10-03"):
    return client.post(
        "/expenses",
        json={"category_id": category_id, "amount": amount, "spent_on": spent_on},
        headers=headers,
    )

def test_create_expense(client, auth_headers):
    cat_id = create_category(client, auth_headers)

    response = create_expense(client, auth_headers, cat_id)

    assert response.status_code == 201
    data = response.json()
    assert data["amount"] == "45.30"
    assert data["currency"] == "EUR"        # default
    assert data["category_id"] == cat_id


def test_create_expense_invalid_category(client, auth_headers):
    response = create_expense(client, auth_headers, category_id=999)

    assert response.status_code == 400


def test_create_expense_negative_amount(client, auth_headers):
    cat_id = create_category(client, auth_headers)

    response = create_expense(client, auth_headers, cat_id, amount="-5")

    assert response.status_code == 422


def test_get_expense(client, auth_headers):
    cat_id = create_category(client, auth_headers)
    expense_id = create_expense(client, auth_headers, cat_id).json()["id"]

    response = client.get(f"/expenses/{expense_id}", headers=auth_headers)

    assert response.status_code == 200
    assert response.json()["id"] == expense_id


def test_get_expense_not_found(client, auth_headers):
    response = client.get("/expenses/999", headers=auth_headers)

    assert response.status_code == 404


def test_update_expense(client, auth_headers):
    cat_id = create_category(client, auth_headers)
    expense_id = create_expense(client, auth_headers, cat_id).json()["id"]

    response = client.put(
        f"/expenses/{expense_id}",
        json={"category_id": cat_id, "amount": "99.99", "spent_on": "2026-10-04"},
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.json()["amount"] == "99.99"


def test_delete_expense(client, auth_headers):
    cat_id = create_category(client, auth_headers)
    expense_id = create_expense(client, auth_headers, cat_id).json()["id"]

    response = client.delete(f"/expenses/{expense_id}", headers=auth_headers)
    assert response.status_code == 204

    assert client.get(f"/expenses/{expense_id}", headers=auth_headers).status_code == 404

def test_list_filter_by_category(client, auth_headers):
    hrana = create_category(client, auth_headers, "Hrana")
    prijevoz = create_category(client, auth_headers, "Prijevoz")
    create_expense(client, auth_headers, hrana)
    create_expense(client, auth_headers, hrana)
    create_expense(client, auth_headers, prijevoz)

    response = client.get(f"/expenses?category_id={hrana}", headers=auth_headers)

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_list_filter_min_amount(client, auth_headers):
    cat_id = create_category(client, auth_headers)
    create_expense(client, auth_headers, cat_id, amount="10.00")
    create_expense(client, auth_headers, cat_id, amount="50.00")

    response = client.get("/expenses?min_amount=20", headers=auth_headers)

    assert len(response.json()) == 1
    assert response.json()[0]["amount"] == "50.00"


def test_summary(client, auth_headers):
    cat_id = create_category(client, auth_headers)
    create_expense(client, auth_headers, cat_id, amount="10.50")
    create_expense(client, auth_headers, cat_id, amount="20.25")

    response = client.get("/expenses/summary", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["number_of_expenses"] == 2
    assert float(data["sum_of_expenses"]) == 30.75

def test_user_cannot_see_other_users_expenses(client, auth_headers, other_auth_headers):
    cat_id = create_category(client, auth_headers)
    create_expense(client, auth_headers, cat_id)

    response = client.get("/expenses", headers=other_auth_headers)

    assert response.status_code == 200
    assert response.json() == []


def test_user_cannot_access_other_users_expense(client, auth_headers, other_auth_headers):
    cat_id = create_category(client, auth_headers)
    expense_id = create_expense(client, auth_headers, cat_id).json()["id"]

    assert client.get(f"/expenses/{expense_id}", headers=other_auth_headers).status_code == 404
    assert client.delete(f"/expenses/{expense_id}", headers=other_auth_headers).status_code == 404

    # Anin trošak je i dalje tu
    assert client.get(f"/expenses/{expense_id}", headers=auth_headers).status_code == 200


def test_user_cannot_use_other_users_category(client, auth_headers, other_auth_headers):
    ana_category = create_category(client, auth_headers)

    response = create_expense(client, other_auth_headers, ana_category)

    assert response.status_code == 400


def test_user_cannot_see_other_users_categories(client, auth_headers, other_auth_headers):
    create_category(client, auth_headers, "Hrana")

    response = client.get("/categories", headers=other_auth_headers)

    assert response.json() == []
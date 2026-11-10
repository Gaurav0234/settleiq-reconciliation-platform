
def register_and_login(client):
    client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "Partner Test User",
            "email": "partner.test@example.com",
            "password": "StrongPassword@123",
        },
    )

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "partner.test@example.com",
            "password": "StrongPassword@123",
        },
    )

    return response.json()["access_token"]


def test_create_partner(client):
    token = register_and_login(client)

    response = client.post(
        "/api/v1/partners",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Shiprocket",
            "partner_type": "courier",
        },
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Shiprocket"
    assert response.json()["partner_type"] == "courier"
    assert response.json()["is_active"] is True


def test_duplicate_partner_is_rejected(client):
    token = register_and_login(client)
    headers = {"Authorization": f"Bearer {token}"}

    payload = {
        "name": "Shiprocket",
        "partner_type": "courier",
    }

    first = client.post("/api/v1/partners", headers=headers, json=payload)
    second = client.post("/api/v1/partners", headers=headers, json=payload)

    assert first.status_code == 201
    assert second.status_code == 409


def test_invalid_partner_type_is_rejected(client):
    token = register_and_login(client)

    response = client.post(
        "/api/v1/partners",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Invalid Partner",
            "partner_type": "payment_gateway",
        },
    )

    assert response.status_code == 422


def test_list_partners(client):
    token = register_and_login(client)
    headers = {"Authorization": f"Bearer {token}"}

    client.post(
        "/api/v1/partners",
        headers=headers,
        json={"name": "Shiprocket", "partner_type": "courier"},
    )

    response = client.get("/api/v1/partners", headers=headers)

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Shiprocket"


def test_retrieve_partner(client):
    token = register_and_login(client)
    headers = {"Authorization": f"Bearer {token}"}

    created = client.post(
        "/api/v1/partners",
        headers=headers,
        json={"name": "Delhivery", "partner_type": "courier"},
    )

    partner_id = created.json()["id"]

    response = client.get(
        f"/api/v1/partners/{partner_id}",
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Delhivery"


def test_update_partner(client):
    token = register_and_login(client)
    headers = {"Authorization": f"Bearer {token}"}

    created = client.post(
        "/api/v1/partners",
        headers=headers,
        json={"name": "Blue Dart", "partner_type": "courier"},
    )

    partner_id = created.json()["id"]

    response = client.patch(
        f"/api/v1/partners/{partner_id}",
        headers=headers,
        json={"is_active": False},
    )

    assert response.status_code == 200
    assert response.json()["is_active"] is False


def test_inactive_partner_is_hidden_by_default(client):
    token = register_and_login(client)
    headers = {"Authorization": f"Bearer {token}"}

    created = client.post(
        "/api/v1/partners",
        headers=headers,
        json={"name": "Inactive Partner", "partner_type": "courier"},
    )

    partner_id = created.json()["id"]

    client.patch(
        f"/api/v1/partners/{partner_id}",
        headers=headers,
        json={"is_active": False},
    )

    response = client.get("/api/v1/partners", headers=headers)

    assert response.status_code == 200
    assert response.json() == []


def test_partner_creation_requires_authentication(client):
    response = client.post(
        "/api/v1/partners",
        json={"name": "Shiprocket", "partner_type": "courier"},
    )

    assert response.status_code == 401



def test_partner_name_with_only_whitespace_is_rejected(client):
    token = register_and_login(client)

    response = client.post(
        "/api/v1/partners",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "   ",
            "partner_type": "courier",
        },
    )

    assert response.status_code == 422


def test_empty_partner_update_is_rejected(client):
    token = register_and_login(client)
    headers = {"Authorization": f"Bearer {token}"}

    created = client.post(
        "/api/v1/partners",
        headers=headers,
        json={
            "name": "Shiprocket",
            "partner_type": "courier",
        },
    )

    partner_id = created.json()["id"]

    response = client.patch(
        f"/api/v1/partners/{partner_id}",
        headers=headers,
        json={},
    )

    assert response.status_code == 422

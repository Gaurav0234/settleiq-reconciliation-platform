
def test_register_user_successfully(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "Test User",
            "email": "test@example.com",
            "password": "StrongPassword@123",
        },
    )

    assert response.status_code == 201
    data = response.json()

    assert data["full_name"] == "Test User"
    assert data["email"] == "test@example.com"
    assert data["role"] == "finance_executive"
    assert data["is_active"] is True
    assert "hashed_password" not in data
    assert "password" not in data


def test_duplicate_email_registration_is_rejected(client):
    payload = {
        "full_name": "Test User",
        "email": "test@example.com",
        "password": "StrongPassword@123",
    }

    first_response = client.post("/api/v1/auth/register", json=payload)
    second_response = client.post("/api/v1/auth/register", json=payload)

    assert first_response.status_code == 201
    assert second_response.status_code == 409


def test_login_with_correct_credentials(client):
    client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "Test User",
            "email": "test@example.com",
            "password": "StrongPassword@123",
        },
    )

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "test@example.com",
            "password": "StrongPassword@123",
        },
    )

    assert response.status_code == 200
    data = response.json()

    assert data["token_type"] == "bearer"
    assert "access_token" in data
    assert len(data["access_token"]) > 0


def test_login_with_wrong_password_is_rejected(client):
    client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "Test User",
            "email": "test@example.com",
            "password": "StrongPassword@123",
        },
    )

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "test@example.com",
            "password": "WrongPassword@123",
        },
    )

    assert response.status_code == 401


def test_get_current_user_with_valid_token(client):
    client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "Test User",
            "email": "test@example.com",
            "password": "StrongPassword@123",
        },
    )

    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "test@example.com",
            "password": "StrongPassword@123",
        },
    )

    token = login_response.json()["access_token"]

    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"


def test_get_current_user_without_token_is_rejected(client):
    response = client.get("/api/v1/auth/me")

    assert response.status_code == 401
    assert response.json()["detail"] == "Authentication required"


def test_get_current_user_with_invalid_token_is_rejected(client):
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": "Bearer invalid.token.value"},
    )

    assert response.status_code == 401

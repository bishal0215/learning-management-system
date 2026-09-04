def test_signup_creates_user(client):
    response = client.post(
        "/auth/signup",
        json={
            "username": "testuser1",
            "email": "testuser1@example.com",
            "password": "testpassword123",
        },
    )

    assert response.status_code ==201

    data = response.json()
    assert data["username"] == "testuser1"
    assert data["email"]==  "testuser1@example.com"
    assert data["is_active"] is True
    assert data["is_superuser"] is False
    assert "password" not in data

def test_login_returns_different_tokens(client):
    client.post(
        "/auth/signup",
        json={
            "username": "loginuser",
            "email":"loginuser@example.com",
            "password":"testpassword123",

        }
    )

    response = client.post(
        "/auth/login",
        data={"username":"loginuser","password":"testpassword123"},

    )

    # 3. ASSERT - check the response is correct
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["access_token"] != data["refresh_token"]
    assert data["token_type"] == "bearer"

def test_login_returns_different_tokens(client, existing_user):
    response = client.post(
        "/auth/login",
        data={"username": existing_user["username"], "password": existing_user["password"]},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["access_token"] != data["refresh_token"]


def test_wrong_user(client, existing_user):
    response = client.post(
        "/auth/login",
        data={"username": existing_user["username"], "password": "wrongpassword"},
    )
    assert response.status_code == 403
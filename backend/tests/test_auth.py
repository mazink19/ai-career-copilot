def test_register(client):
    response = client.post(
        "/auth/register",
        json={
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 201

def test_register_duplicate_email(client):
    payload = {
        "first_name": "Test",
        "last_name": "User",
        "email": "duplicate@example.com",
        "password": "password123",
    }

    first_response = client.post(
        "/auth/register",
        json=payload,
    )

    print(first_response.status_code)
    print(first_response.json())

    second_response = client.post(
        "/auth/register",
        json=payload,
    )

    print(second_response.status_code)
    print(second_response.json())

    assert second_response.status_code == 409

def test_login(client):
    # Register user first
    client.post(
        "/auth/register",
        json={
            "first_name": "Test",
            "last_name": "User",
            "email": "login@example.com",
            "password": "password123",
        },
    )

    # Login
    response = client.post(
        "/auth/login",
        json={
            "email": "login@example.com",
            "password": "password123",
        },
    )
    print(response.status_code)
    print(response.json())
    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"    


def test_login_wrong_password(client):
    client.post(
        "/auth/register",
        json={
            "first_name": "Test",
            "last_name": "User",
            "email": "wrong@example.com",
            "password": "password123",
        },
    )

    response = client.post(
        "/auth/login",
        json={
            "email": "wrong@example.com",
            "password": "wrong-password",
        },
    )

    assert response.status_code == 401


def test_get_current_user(client):
    # Register
    client.post(
        "/auth/register",
        json={
            "first_name": "Test",
            "last_name": "User",
            "email": "me@example.com",
            "password": "password123",
        },
    )

    # Login
    login_response = client.post(
        "/auth/login",
        json={
            "email": "me@example.com",
            "password": "password123",
        },
    )

    token = login_response.json()["access_token"]

    # Access protected endpoint
    response = client.get(
        "/auth/me",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["email"] == "me@example.com"
    assert data["first_name"] == "Test"
    assert data["last_name"] == "User"    

def test_get_current_user_without_token(client):
    response = client.get("/auth/me")

    assert response.status_code == 401


def test_get_resumes(client):
    client.post(
        "/auth/register",
        json={
            "first_name": "Test",
            "last_name": "User",
            "email": "list@example.com",
            "password": "password123",
        },
    )

    login_response = client.post(
        "/auth/login",
        json={
            "email": "list@example.com",
            "password": "password123",
        },
    )

    token = login_response.json()["access_token"]

    with open("tests/files/test_resume.pdf", "rb") as file:
        upload_response = client.post(
            "/resumes/upload",
            headers={"Authorization": f"Bearer {token}"},
            files={
                "file": (
                    "test_resume.pdf",
                    file,
                    "application/pdf",
                )
            },
        )

    assert upload_response.status_code == 201

    response = client.get(
        "/resumes",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["file_name"] == "test_resume.pdf"
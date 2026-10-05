from fastapi.testclient import TestClient


def test_upload_resume(client: TestClient):
    # Register
    client.post(
        "/auth/register",
        json={
            "first_name": "Test",
            "last_name": "User",
            "email": "resume@example.com",
            "password": "password123",
        },
    )

    # Login
    login_response = client.post(
        "/auth/login",
        json={
            "email": "resume@example.com",
            "password": "password123",
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    # Upload PDF
    with open("tests/files/test_resume.pdf", "rb") as file:
        response = client.post(
            "/resumes/upload",
            headers={
                "Authorization": f"Bearer {token}",
            },
            files={
                "file": (
                    "test_resume.pdf",
                    file,
                    "application/pdf",
                )
            },
        )

    assert response.status_code == 201

    # Get created resume ID
    resume_id = response.json()["id"]

    # Get AI analysis
    analysis_response = client.get(
        f"/resumes/{resume_id}/analysis",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert analysis_response.status_code == 200

    analysis = analysis_response.json()

    # Verify analysis belongs to this resume
    assert analysis["resume_id"] == resume_id

    # Verify AI analysis contains data
    assert analysis["summary"]
    assert analysis["skills"]
    assert analysis["education"]
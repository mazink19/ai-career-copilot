
from app.db.models.resume import Resume
from app.db.models.user import User


def test_get_job(client):

    create = client.post(
        "/jobs",
        json={
            "source": "manual",
            "external_id": "test-job-123",  
            "title": "Backend Engineer",
            "company": "Example Corp",
            "description": "Build APIs",
            "application_url": "https://example.com/jobs/456",
        },
    )

    job_id = create.json()["id"]

    response = client.get(f"/jobs/{job_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == job_id
    assert data["title"] == "Backend Engineer"

def test_get_jobs(client):

    client.post(
        "/jobs",
        json={
            "title": "AI Engineer",
            "company": "Company A",
            "description": "AI work",
            "application_url": "https://example.com/ai",
        },
    )

    client.post(
        "/jobs",
        json={
            "title": "Backend Engineer",
            "company": "Company B",
            "description": "Backend work",
            "application_url": "https://example.com/backend",
        },
    )

    response = client.get("/jobs")

    assert response.status_code == 200
    data = response.json()

    assert len(data["jobs"]) == 2
    assert data["total"] == 2
    
def test_get_job_not_found(client):

    response = client.get("/jobs/999999")

    assert response.status_code == 404

def test_apply_to_job(client):

    create = client.post(
        "/jobs",
        json={
            "title": "AI Engineer",
            "company": "Example Corp",
            "description": "Build AI applications",
            "application_url": "https://example.com/jobs/123",
        },
    )

    job_id = create.json()["id"]

    response = client.get(
        f"/jobs/{job_id}/apply"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["application_url"] == "https://example.com/jobs/123"

def test_apply_to_nonexistent_job(client):

    response = client.get("/jobs/999999/apply")

    assert response.status_code == 404


def test_match_job(client):

    # Register
    client.post(
        "/auth/register",
        json={
            "first_name": "Test",
            "last_name": "User",
            "email": "jobmatch@example.com",
            "password": "password123",
        },
    )

    # Login
    login = client.post(
        "/auth/login",
        json={
            "email": "jobmatch@example.com",
            "password": "password123",
        },
    )

    token = login.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}",
    }

    # Create job
    job_response = client.post(
        "/jobs",
        headers=headers,
        json={
            "title": "AI Engineer",
            "company": "Example Corp",
            "description": """
                We are looking for an AI Engineer with
                Python, FastAPI, PostgreSQL, Docker and LangChain.
            """,
            "application_url": "https://example.com/jobs/123",
        },
    )

    assert job_response.status_code == 201

    job_id = job_response.json()["id"]

    # Upload resume
    with open("tests/files/test_resume.pdf", "rb") as file:
        resume_response = client.post(
            "/resumes/upload",
            headers=headers,
            files={
                "file": (
                    "test_resume.pdf",
                    file,
                    "application/pdf",
                )
            },
        )

    assert resume_response.status_code == 201

    # Match resume against job
    response = client.post(
        f"/jobs/{job_id}/match",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert "score" in data
    assert 0 <= data["score"] <= 100

    assert "matched_skills" in data
    assert "missing_skills" in data
    assert "strengths" in data
    assert "recommendations" in data


def test_match_nonexistent_job(client):

    # Register
    client.post(
        "/auth/register",
        json={
            "first_name": "Test",
            "last_name": "User",
            "email": "nojob@example.com",
            "password": "password123",
        },
    )

    # Login
    login = client.post(
        "/auth/login",
        json={
            "email": "nojob@example.com",
            "password": "password123",
        },
    )

    token = login.json()["access_token"]

    response = client.post(
        "/jobs/99999/match",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 404


def test_match_without_resume(client):

    client.post(
        "/auth/register",
        json={
            "first_name": "Test",
            "last_name": "User",
            "email": "noresume@example.com",
            "password": "password123",
        },
    )

    login = client.post(
        "/auth/login",
        json={
            "email": "noresume@example.com",
            "password": "password123",
        },
    )

    token = login.json()["access_token"]

    job_response = client.post(
        "/jobs",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "title": "AI Engineer",
            "company": "Example Corp",
            "description": "Python FastAPI Docker",
            "application_url": "https://example.com/jobs/123",
        },
    )

    job_id = job_response.json()["id"]

    response = client.post(
        f"/jobs/{job_id}/match",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 404    



def test_match_without_resume_analysis(client, db):

    # Register user
    client.post(
        "/auth/register",
        json={
            "first_name": "Test",
            "last_name": "User",
            "email": "noanalysis@example.com",
            "password": "password123",
        },
    )

    # Login
    login = client.post(
        "/auth/login",
        json={
            "email": "noanalysis@example.com",
            "password": "password123",
        },
    )

    token = login.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}",
    }

    # Create job
    job_response = client.post(
        "/jobs",
        headers=headers,
        json={
            "title": "AI Engineer",
            "company": "Example Corp",
            "description": "Python FastAPI Docker",
            "application_url": "https://example.com/jobs/123",
        },
    )

    assert job_response.status_code == 201

    job_id = job_response.json()["id"]

    # Get the user from the database
    user = db.query(User).filter(
        User.email == "noanalysis@example.com"
    ).first()

    assert user is not None

    # Create resume directly.
    # We intentionally DO NOT create ResumeAnalysis.
    resume = Resume(
        user_id=user.id,
        file_name="test_resume.pdf",
        file_path="tests/files/test_resume.pdf",
    )

    db.add(resume)
    db.commit()

    # Try to match
    response = client.post(
        f"/jobs/{job_id}/match",
        headers=headers,
    )

    assert response.status_code == 404    


    
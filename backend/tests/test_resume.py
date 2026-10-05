import pytest

from app.ai.extraction.pdf_extractior import PDFExtractor
from app.db.models.analysis_status import AnalysisStatus
from app.db.models.resume_analysis import ResumeAnalysis
from app.repositories.resume_analysis_repository import ResumeAnalysisRepository
from app.services.resume_analysis_service import ResumeAnalysisService

from tests.fakes.failing_resume_analyzer import FailingResumeAnalyzer

def test_upload_resume(client):
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

    data = response.json()

    assert data["file_name"] == "test_resume.pdf"
    assert "id" in data
    assert "uploaded_at" in data


def test_user_cannot_access_other_users_resume(client):
    # User 1
    client.post(
        "/auth/register",
        json={
            "first_name": "User",
            "last_name": "One",
            "email": "user1@example.com",
            "password": "password123",
        },
    )

    login1 = client.post(
        "/auth/login",
        json={
            "email": "user1@example.com",
            "password": "password123",
        },
    )

    token1 = login1.json()["access_token"]

    # User 1 uploads resume
    with open("tests/files/test_resume.pdf", "rb") as file:
        upload = client.post(
            "/resumes/upload",
            headers={
                "Authorization": f"Bearer {token1}"
            },
            files={
                "file": (
                    "test_resume.pdf",
                    file,
                    "application/pdf",
                )
            },
        )

    assert upload.status_code == 201

    resume_id = upload.json()["id"]

    # User 2
    client.post(
        "/auth/register",
        json={
            "first_name": "User",
            "last_name": "Two",
            "email": "user2@example.com",
            "password": "password123",
        },
    )

    login2 = client.post(
        "/auth/login",
        json={
            "email": "user2@example.com",
            "password": "password123",
        },
    )

    token2 = login2.json()["access_token"]

    # User 2 tries to access User 1's resume
    response = client.delete(
        f"/resumes/{resume_id}",
        headers={
            "Authorization": f"Bearer {token2}",
        },
    )

    assert response.status_code == 403


def test_user_cannot_access_other_users_resume_analysis(client):
    # User 1
    client.post(
        "/auth/register",
        json={
            "first_name": "User",
            "last_name": "One",
            "email": "analysis_user1@example.com",
            "password": "password123",
        },
    )

    # Login User 1
    login1 = client.post(
        "/auth/login",
        json={
            "email": "analysis_user1@example.com",
            "password": "password123",
        },
    )

    token1 = login1.json()["access_token"]

    # User 1 uploads resume
    with open("tests/files/test_resume.pdf", "rb") as file:
        upload = client.post(
            "/resumes/upload",
            headers={
                "Authorization": f"Bearer {token1}",
            },
            files={
                "file": (
                    "test_resume.pdf",
                    file,
                    "application/pdf",
                )
            },
        )

    assert upload.status_code == 201

    resume_id = upload.json()["id"]

    # User 2
    client.post(
        "/auth/register",
        json={
            "first_name": "User",
            "last_name": "Two",
            "email": "analysis_user2@example.com",
            "password": "password123",
        },
    )

    # Login User 2
    login2 = client.post(
        "/auth/login",
        json={
            "email": "analysis_user2@example.com",
            "password": "password123",
        },
    )

    token2 = login2.json()["access_token"]

    # User 2 tries to access User 1's resume analysis
    response = client.get(
        f"/resumes/{resume_id}/analysis",
        headers={
            "Authorization": f"Bearer {token2}",
        },
    )

    assert response.status_code == 403


def test_user_can_access_own_resume_analysis(client):
    # Register
    client.post(
        "/auth/register",
        json={
            "first_name": "Test",
            "last_name": "User",
            "email": "analysis_owner@example.com",
            "password": "password123",
        },
    )

    # Login
    login = client.post(
        "/auth/login",
        json={
            "email": "analysis_owner@example.com",
            "password": "password123",
        },
    )

    token = login.json()["access_token"]

    # Upload resume
    with open("tests/files/test_resume.pdf", "rb") as file:
        upload = client.post(
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

    assert upload.status_code == 201

    resume_id = upload.json()["id"]

    # Get own analysis
    response = client.get(
        f"/resumes/{resume_id}/analysis",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["summary"] == "Test resume summary"
    assert data["skills"] == [
        "Python",
        "FastAPI",
    ]
    assert data["education"] == ["Computer Science"]
    assert data["projects"] == ["AI Career Copilot"]    
def test_resume_analysis_lifecycle(client):
    # Register
    client.post(
        "/auth/register",
        json={
            "first_name": "Test",
            "last_name": "User",
            "email": "lifecycle@example.com",
            "password": "password123",
        },
    )

    # Login
    login = client.post(
        "/auth/login",
        json={
            "email": "lifecycle@example.com",
            "password": "password123",
        },
    )

    token = login.json()["access_token"]

    # Upload resume
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

    resume_id = response.json()["id"]

    # Get analysis
    response = client.get(
        f"/resumes/{resume_id}/analysis",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"].lower() == "completed"

## Test the failing analyzer

def test_resume_analysis_failure(db):
    repository = ResumeAnalysisRepository(db)

    service = ResumeAnalysisService(
        analysis_repository=repository,
        extractor=PDFExtractor(),
        analyzer=FailingResumeAnalyzer(),
    )

    service.analyze_resume(
        file_path="tests/files/test_resume.pdf",
        resume_id=1,
    )

    analysis = repository.get_by_resume_id(1)

    assert analysis is not None
    assert analysis.status == AnalysisStatus.FAILED
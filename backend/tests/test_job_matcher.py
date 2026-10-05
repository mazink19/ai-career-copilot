from app.ai.analyzers.job_matcher import JobMatcher
from app.schemas.ai.job_match_analysis import JobMatchAnalysis
from app.schemas.ai.resume_analysis import ResumeAnalysis


def test_job_matcher():

    matcher = JobMatcher()

    resume = ResumeAnalysis(
        summary="Python backend developer with experience building AI applications.",
        skills=[
            "Python",
            "FastAPI",
            "PostgreSQL",
            "Docker",
            "LangChain",
        ],
        experience=[
            "Backend Developer Intern at ABC Company"
        ],
        education=[
            "BSc Computer Science"
        ],
        projects=[
            "Built an AI Career Copilot using FastAPI and LangChain"
        ],
    )

    job_description = """
    We are looking for an AI Engineer.

    Requirements:
    - Python
    - FastAPI
    - PostgreSQL
    - Docker
    - LangChain
    - Experience building AI applications
    """

    result = matcher.match(
        resume=resume,
        job_description=job_description,
    )

    print("\n", result)

    assert isinstance(result, JobMatchAnalysis)
    assert 0 <= result.score <= 100
    assert result.strengths
    assert result.missing_skills is not None
    assert result.recommendations
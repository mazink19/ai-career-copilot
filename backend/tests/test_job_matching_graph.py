from app.ai.analyzers.job_matcher import JobMatcher
from app.schemas.ai.resume_analysis import ResumeAnalysis
from app.graph.job_matching.workflow import build_job_matching_graph
from app.graph.job_matching.nodes import route_match
from app.graph.job_matching.nodes import make_analyze_match_node
from tests.fakes.fake_job_matcher import FakeJobMatcher
from app.graph.job_matching.workflow import build_job_matching_graph
from tests.fakes.fake_job_matcher import (
    FakeJobMatcher,
    WeakFakeJobMatcher,
)


def test_job_matching_graph():

    matcher = JobMatcher()

    graph = build_job_matching_graph(matcher)

    resume = ResumeAnalysis(
        summary="Python backend developer",
        skills=[
            "Python",
            "FastAPI",
            "PostgreSQL",
            "Docker",
        ],
        experience=[
            "Backend Developer"
        ],
        education=[
            "BSc Computer Science"
        ],
        projects=[
            "AI Career Copilot"
        ],
    )

    result = graph.invoke({
        "resume": resume,
        "job_description": """
        We need an AI Engineer with:

        Python
        FastAPI
        PostgreSQL
        Docker
        LangChain
        """,
    })

    assert result["resume"] == resume
    assert result["job_description"]
    assert result["analysis"]
    assert result["score"] >= 0
    assert result["score"] <= 100

def test_job_matching_graph_routes():

    matcher = JobMatcher()

    graph = build_job_matching_graph(matcher)

    resume = ResumeAnalysis(
        summary="Python backend developer",
        skills=[
            "Python",
            "FastAPI",
            "PostgreSQL",
            "Docker",
            "LangChain",
        ],
        experience=["Backend Developer"],
        education=["BSc Computer Science"],
        projects=["AI Career Copilot"],
    )

    result = graph.invoke({
        "resume": resume,
        "job_description": """
        We need an AI Engineer with Python,
        FastAPI, PostgreSQL, Docker and LangChain.
        """,
    })

    assert result["analysis"]
    assert result["score"] >= 0
    assert result["score"] <= 100
    assert result["recommendation"]


def test_analyze_match_node():

    matcher = FakeJobMatcher()

    node = make_analyze_match_node(matcher)

    state = {
        "resume": None,
        "job_description": "Python FastAPI engineer",
    }

    result = node(state)

    assert result["score"] == 85
    assert result["analysis"].score == 85
    assert result["analysis"].matched_skills == [
        "Python",
        "FastAPI",
        "PostgreSQL",
    ]


def test_route_good_match():

    state = {
        "score": 85,
    }

    assert route_match(state) == "good_match"


def test_route_weak_match():

    state = {
        "score": 60,
    }

    assert route_match(state) == "weak_match"



def test_job_matching_graph_good_match():

    graph = build_job_matching_graph(FakeJobMatcher())

    result = graph.invoke({
        "resume": None,
        "job_description": "Python FastAPI engineer",
    })

    assert result["score"] == 85
    assert result["analysis"].score == 85
    assert result["recommendation"] == (
        "Strong match. Apply for this job."
    )


def test_job_matching_graph_weak_match():

    graph = build_job_matching_graph(WeakFakeJobMatcher())

    result = graph.invoke({
        "resume": None,
        "job_description": "Senior AI Engineer",
    })

    assert result["score"] == 50
    assert result["analysis"].score == 50
    assert result["recommendation"] == (
        "Weak match. Consider improving your missing skills."
    )

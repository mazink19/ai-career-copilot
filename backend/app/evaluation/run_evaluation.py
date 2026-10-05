from app.evaluation.evaluators import evaluate_skills
from app.schemas.ai.job_match_analysis import JobMatchAnalysis


output = JobMatchAnalysis(
    score=85,
    matched_skills=[
        "Python",
        "FastAPI",
        "LangGraph",
        "RAG",
    ],
    missing_skills=[
        "PyTorch",
    ],
    strengths=[
        "Strong LLM application experience",
    ],
    recommendations=[
        "Learn PyTorch",
    ],
)

reference = {
    "matched_skills": [
        "Python",
        "FastAPI",
        "LangGraph",
        "RAG",
    ],
    "missing_skills": [
        "PyTorch",
    ],
}

result = evaluate_skills(output, reference)

print(result)
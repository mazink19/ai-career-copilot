from app.schemas.ai.resume_analysis import ResumeAnalysis


class FakeResumeAnalyzer:
    def analyze(self, resume_text: str) -> ResumeAnalysis:
        return ResumeAnalysis(
            summary="Test resume summary",
            skills=["Python", "FastAPI"],
            experience=["Backend Engineer"],
            education=["Computer Science"],
            projects=["AI Career Copilot"],
        )
from app.schemas.ai.job_match_analysis import JobMatchAnalysis


class FakeJobMatcher:

    def match(
        self,
        resume,
        job_description: str,
    ) -> JobMatchAnalysis:

        return JobMatchAnalysis(
            score=85,
            matched_skills=[
                "Python",
                "FastAPI",
                "PostgreSQL",
            ],
            missing_skills=[
                "Kubernetes",
            ],
            strengths=[
                "Strong backend development experience",
                "Experience building AI applications",
            ],
            recommendations=[
                "Apply for this position",
            ],
        )
    
class WeakFakeJobMatcher:

    def match(self, resume, job_description: str) -> JobMatchAnalysis:
        return JobMatchAnalysis(
            score=50,
            matched_skills=["Python"],
            missing_skills=["FastAPI", "Docker"],
            strengths=["Basic Python experience"],
            recommendations=["Improve FastAPI and Docker skills"],
        )    

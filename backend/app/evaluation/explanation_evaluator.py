from app.evaluation.judges import ExplanationJudge


class ExplanationEvaluator:
    def __init__(self):
        self.judge = ExplanationJudge()

    def evaluate(
        self,
        resume: dict,
        job_description: str,
        matched_skills: list[str],
        missing_skills: list[str],
        strengths: list[str],
        recommendations: list[str],
        reference_strengths: list[str],
        reference_recommendations: list[str],
    ) -> dict:

        result = self.judge.evaluate(
            resume=resume,
            job_description=job_description,
            matched_skills=matched_skills,
            missing_skills=missing_skills,
            strengths=strengths,
            recommendations=recommendations,
        )

        return {
            "strengths_quality": result.strengths_score / 100,
            "recommendations_quality": result.recommendations_score / 100,
        }
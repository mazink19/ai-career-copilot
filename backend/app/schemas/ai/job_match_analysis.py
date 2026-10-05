from pydantic import BaseModel, Field


class JobMatchAnalysis(BaseModel):
    score: int = Field(ge=0, le=100)
    matched_skills: list[str]
    missing_skills: list[str]
    strengths: list[str]
    recommendations: list[str]
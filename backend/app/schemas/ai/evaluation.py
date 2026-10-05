from pydantic import BaseModel, Field


class ExplanationEvaluation(BaseModel):
    strengths_score: int = Field(ge=0, le=100)
    recommendations_score: int = Field(ge=0, le=100)
    overall_score: int = Field(ge=0, le=100)

    strengths_reason: str
    recommendations_reason: str
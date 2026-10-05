from app.ai.llm.client import get_llm
from app.ai.prompts.job_mathcing import job_matching_prompt
from app.schemas.ai.job_match_analysis import JobMatchAnalysis
from app.schemas.ai.resume_analysis import ResumeAnalysis


class JobMatcher:

    def __init__(self):
        llm = get_llm()

        self.chain = (
            job_matching_prompt
            | llm.with_structured_output(
                JobMatchAnalysis,
                method="json_schema",
                strict=True
            )
        )

    def match(
        self,
        resume: ResumeAnalysis,
        job_description: str,
    ) -> JobMatchAnalysis:

        return self.chain.invoke(
            {
                "resume": resume.model_dump(),
                "job_description": job_description,
            }
        )
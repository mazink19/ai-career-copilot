from app.ai.llm.client import get_llm
from app.ai.prompts.resume_analysis import resume_analysis_prompt
from app.schemas.ai.resume_analysis import ResumeAnalysis


class ResumeAnalyzer:

    def __init__(self):
        llm = get_llm()

        self.chain = (
            resume_analysis_prompt
            | llm.with_structured_output(ResumeAnalysis)
        )

    def analyze(self, resume_text: str) -> ResumeAnalysis:
        return self.chain.invoke(
            {"resume_text": resume_text}
        )
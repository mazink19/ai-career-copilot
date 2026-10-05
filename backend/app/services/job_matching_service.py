from app.core.exceptions import NotFoundException

from app.schemas.ai.job_match_analysis import JobMatchAnalysis

from app.mappers.resume_analysis import to_ai_schema

from app.repositories.resume_analysis_repository import ResumeAnalysisRepository
from app.repositories.job_repository import JobRepository
from app.repositories.resume_repository import ResumeRepository

from app.ai.analyzers.job_matcher import JobMatcher
from app.graph.job_matching.workflow import build_job_matching_graph

class JobMatchingService:

    def __init__(
        self,
        job_repository: JobRepository,
        resume_repository: ResumeRepository,
        analysis_repository: ResumeAnalysisRepository,
        matcher: JobMatcher,
    ):
        self.job_repository = job_repository
        self.resume_repository = resume_repository
        self.analysis_repository = analysis_repository

        self.graph = build_job_matching_graph(matcher)

    def match_job(self,user_id: int,job_id: int,) -> JobMatchAnalysis:

        job = self.job_repository.get_by_id(job_id)

        if job is None:
            raise NotFoundException("Job not found")

        resume = self.resume_repository.get_by_user_id(user_id)

        if resume is None:
            raise NotFoundException("Resume not found")

        resume_analysis = (self.analysis_repository.get_by_resume_id(resume.id))

        if resume_analysis is None:
            raise NotFoundException("Resume analysis not found")
        ai_resume = to_ai_schema(resume_analysis)
        result = self.graph.invoke(
            {
                "resume": ai_resume,
                "job_description": job.description,
            }
        )

        return result["analysis"]
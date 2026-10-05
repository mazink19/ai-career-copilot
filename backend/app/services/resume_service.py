from pathlib import Path
from fastapi import UploadFile
from sqlalchemy.orm import Session
from uuid import uuid4

from app.core.exceptions import(NotFoundException, ForbiddenException, ValidationExecption)

from app.db.models.resume import Resume
from app.db.models.user import User

from app.schemas.resume import ResumeResponse

from app.repositories.resume_repository import ResumeRepository
from app.ai.resume_analysis_response import ResumeAnalysisResponse

from app.services.resume_analysis_service import ResumeAnalysisService


class ResumeService:

    UPLOAD_DIR = Path("uploads")
    MAX_FILE_SIZE = 5 * 1024 * 1024 # 5 MB
    def __init__(   
        self,db: Session,analysis_service: ResumeAnalysisService,):
        self.repository = ResumeRepository(db)
        self.analysis_service = analysis_service
        self.UPLOAD_DIR.mkdir(exist_ok=True)


    def upload_resume(self, file: UploadFile, current_user: User):

        if file.content_type != "application/pdf":
            raise ValidationExecption("Only PDF files are allowed")

        if not file.filename or not file.filename.lower().endswith(".pdf"):
            raise ValidationExecption("File must have .pdf extension")

        file.file.seek(0, 2)
        file_size = file.file.tell()
        file.file.seek(0)

        if file_size > self.MAX_FILE_SIZE:
            raise ValidationExecption("File size exceeds the maximum limit of 5 MB")

        unique_name = f"{uuid4()}-{file.filename}"
        destination = self.UPLOAD_DIR / unique_name

        with destination.open("wb") as buffer:
            buffer.write(file.file.read())


        # Create Resume database object
        resume = Resume(
        user_id=current_user.id,
        file_name=file.filename,
        file_path=str(destination),)

        # Save resume first
        saved_resume = self.repository.create(resume)

        self.analysis_service.analyze_resume(
            file_path=str(destination),
            resume_id=saved_resume.id,
            )

        return self._to_response(saved_resume)


    def get_user_resumes(self,current_user: User,) -> list[ResumeResponse]:
        resumes = self.repository.get_by_user(current_user.id)

        return [self._to_response(resume) for resume in resumes]
    

    def _to_response(self, resume: Resume) -> ResumeResponse:
        return ResumeResponse(
            id=resume.id,
            file_name=resume.file_name,
            uploaded_at=resume.uploaded_at,
            analysis_status=(
                resume.analysis.status
                if resume.analysis
                else None
            ),
        )


    def delete_resume(self, resume_id: int, current_user:User)-> None:
        resume = self.repository.get_by_id(resume_id)
        if resume is None:
            raise NotFoundException("Resume not found")
        if resume.user_id != current_user.id:
            raise ForbiddenException("Forbidden")
        file_path = Path(resume.file_path)
        if file_path.exists():
            file_path.unlink()
        self.repository.delete(resume)


    def get_resume_analysis(self,resume_id: int,
                            current_user: User,) -> ResumeAnalysisResponse:
        
        resume = self.repository.get_by_id(resume_id)
        if resume is None:
            raise NotFoundException("Resume not found")

        if resume.user_id != current_user.id:
            raise ForbiddenException("Forbidden")
        
        return self.analysis_service.get_resume_analysis(resume_id)

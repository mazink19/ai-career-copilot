from fastapi import APIRouter, Depends, File, Response, UploadFile, status

from app.ai.resume_analysis_response import ResumeAnalysisResponse
from app.db.models.user import User
from app.dependencies.auth import get_current_user
from app.dependencies.resume import get_resume_service
from app.schemas.resume import ResumeResponse
from app.services.resume_service import ResumeService


router = APIRouter(
    prefix="/resumes",
    tags=["Resumes"],
)


@router.post(
    "/upload",
    response_model=ResumeResponse,
    status_code=status.HTTP_201_CREATED,
)
def upload_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    service: ResumeService = Depends(get_resume_service),
):
    return service.upload_resume(file, current_user)


@router.get(
    "",
    response_model=list[ResumeResponse],
)
def get_resumes(
    current_user: User = Depends(get_current_user),
    service: ResumeService = Depends(get_resume_service),
):
    return service.get_user_resumes(current_user)


@router.delete(
    "/{resume_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_resume(
    resume_id: int,
    current_user: User = Depends(get_current_user),
    service: ResumeService = Depends(get_resume_service),
):
    service.delete_resume(
        resume_id,
        current_user,
    )

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/{resume_id}/analysis",
    response_model=ResumeAnalysisResponse,
)
def get_resume_analysis(
    resume_id: int,
    current_user: User = Depends(get_current_user),
    service: ResumeService = Depends(get_resume_service),
):
    return service.get_resume_analysis(
        resume_id=resume_id,
        current_user=current_user,
    )
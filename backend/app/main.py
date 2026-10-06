from fastapi import FastAPI, Request

from fastapi.responses import JSONResponse

from app.routers.auth import router as auth_router
from app.routers.resume import router as resume_router
from app.routers.jobs import router as jobs_router

from app.core.exceptions import AppException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://ai-career-copilot-zeta-eosin.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router)
app.include_router(resume_router)
app.include_router(jobs_router)


@app.exception_handler(AppException)
async def app_exception_handler(
    request: Request,
    exc: AppException,
):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
    )

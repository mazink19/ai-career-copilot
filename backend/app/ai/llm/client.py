from app.core.config import settings
from langchain_groq import ChatGroq
from app.schemas.ai.resume_analysis import ResumeAnalysis
def get_llm():
    return ChatGroq(
        model="openai/gpt-oss-20b",
        api_key=settings.groq_api_key,
        temperature=0,
    )
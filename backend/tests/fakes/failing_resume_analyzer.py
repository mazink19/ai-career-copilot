class FailingResumeAnalyzer:

    def analyze(self, resume_text: str):
        raise RuntimeError("AI analysis failed")
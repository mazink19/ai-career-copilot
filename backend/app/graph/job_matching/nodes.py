from app.ai.analyzers.job_matcher import JobMatcher


def make_analyze_match_node(matcher: JobMatcher):
    def analyze_match(state):
        result = matcher.match(
        resume=state["resume"],
        job_description=state["job_description"],
    )

        return {
        "analysis": result,
        "score": result.score,
        }

    return analyze_match

def route_match(state):

    if state["score"] >= 75:
        return "good_match"

    return "weak_match"

def good_match_node(state):

    return {
        "recommendation": "Strong match. Apply for this job."
    }


def weak_match_node(state):

    return {
        "recommendation": "Weak match. Consider improving your missing skills."
    }
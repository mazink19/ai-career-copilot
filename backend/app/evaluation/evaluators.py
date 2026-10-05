from app.schemas.ai.job_match_analysis import JobMatchAnalysis


def evaluate_skills(
    output: JobMatchAnalysis,
    reference: dict,
) -> dict:

    predicted_matched = {
        skill.lower()
        for skill in output.matched_skills
    }

    predicted_missing = {
        skill.lower()
        for skill in output.missing_skills
    }

    expected_matched = {
        skill.lower()
        for skill in reference["matched_skills"]
    }

    expected_missing = {
        skill.lower()
        for skill in reference["missing_skills"]
    }

    matched_correct = predicted_matched & expected_matched
    missing_correct = predicted_missing & expected_missing

    total_expected = (
        len(expected_matched)
        + len(expected_missing)
    )

    correct = (
        len(matched_correct)
        + len(missing_correct)
    )

    score = (
        correct / total_expected
        if total_expected > 0
        else 0.0
    )

    return {
        "score": score,
        "matched_skill_accuracy": (
            len(matched_correct) / len(expected_matched)
            if expected_matched
            else 1.0
        ),
        "missing_skill_accuracy": (
            len(missing_correct) / len(expected_missing)
            if expected_missing
            else 1.0
        ),
    }


def evaluate_score(output, reference):
    predicted = output.score
    expected = reference["reference_score"]

    error = abs(predicted - expected)

    # 100 = exact match, 0 = maximally different
    score = max(0.0, 1.0 - (error / 100))

    return {
        "score": score,
        "absolute_error": error,
    }
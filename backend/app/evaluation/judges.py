from langchain_core.prompts import ChatPromptTemplate

from app.ai.llm.client import get_llm
from app.schemas.ai.evaluation import ExplanationEvaluation

explanation_prompt = ChatPromptTemplate.from_template(
    """
You are evaluating the quality of an AI job-matching analysis.

Evaluate whether the generated strengths and recommendations are
accurate, relevant, useful, and supported by the resume and job description.

Resume:
{resume}

Job Description:
{job_description}

Matched Skills:
{matched_skills}

Missing Skills:
{missing_skills}

Generated Strengths:
{strengths}

Reference Strengths:
{reference_strengths}

Generated Recommendations:
{recommendations}

Reference Recommendations:
{reference_recommendations}

Evaluate using these criteria.

STRENGTHS:

Evaluate every generated strength independently.

A good strength must satisfy ALL of these:
1. It is directly supported by information in the resume.
2. It is relevant to the job description.
3. It accurately represents the candidate's actual level of experience.
4. It does not introduce facts that are absent from the resume.

Compare the generated strengths with the reference strengths, but do NOT
assume that a generated strength is correct simply because it expresses a
similar general idea.

Do not require exact wording.

FACTUAL SUPPORT CHECK:

For every generated strength:

1. Identify each factual claim.
2. Find the corresponding evidence in the resume.
3. Determine whether the evidence explicitly supports the claim.
4. Check whether the wording exaggerates the candidate's experience.
5. Penalize unsupported claims even when the general idea is related to
   something in the resume.

The following must NOT be inferred unless explicitly supported by the resume:
- production experience
- leadership
- ownership
- scale
- seniority
- enterprise experience
- team management
- business impact
- measurable results
- specific technologies
- cloud platforms
- deployment environments

IMPORTANT DISTINCTIONS:

"Developed a model" does NOT prove production experience.

"Deployed a model" does NOT automatically prove production experience.

"Built a project" does NOT prove leadership.

"Used Docker" does NOT prove Kubernetes.

"Used Python" does NOT prove experience with a Python framework.

"Worked on an enterprise project" does NOT prove enterprise ownership.

If a generated strength contains multiple claims and one of those claims is
unsupported, penalize the strength for the unsupported claim.

Do not give full credit because the overall idea sounds reasonable.

The specific factual claims must be supported by the resume.

REFERENCE STRENGTHS:

Reference strengths are guidance, not absolute truth.

A generated strength may receive full credit even if it is worded differently
from the reference, provided that its factual claims are supported by the
resume and it is relevant to the job.

A generated strength should NOT receive full credit merely because it matches
the reference if the resume does not support the claim.
Important distinction:
- "developed a model" does NOT prove production experience.
- "deployed a model" does NOT automatically prove production experience.
- "worked on an enterprise project" does NOT prove enterprise ownership.
- "built a project" does NOT prove leadership.
- "used Docker" does NOT prove Kubernetes or cloud experience.

If a strength contains both supported and unsupported claims,
evaluate the unsupported claim as a factual error.

Do not give full credit to a strength merely because its general idea
is related to the resume. The specific factual claims must be supported.

- Treat unsupported additions as factual errors.
- If the generated strength adds information that is not present in the resume,
  penalize it even if the general idea is correct.
- Do not infer production experience, leadership, scale, ownership, seniority,
  or specific technologies unless the resume provides evidence.
- Distinguish between "developed/deployed" and "production experience".
- A strength is only fully correct when both its main claim and its level of
experience are supported by the resume. 

RECOMMENDATIONS:
- Must address actual gaps or opportunities.
- Must be relevant to this specific job.
- Should be concrete and actionable.
- Compare the generated recommendations with the reference recommendations.
- Do not require exact wording.
- Give credit when the generated recommendation addresses the same
  underlying issue using different wording.
- Penalize generic recommendations.
- Do not recommend optional skills when there are no important gaps.

- If the candidate has no meaningful gaps or improvements relevant to the
  job, an empty recommendations list is correct.
- When the reference recommendations are empty and the generated
  recommendations are also empty, give a high recommendations score.
- Do not penalize the model for providing no recommendations when there
  are no meaningful improvements to recommend.

SCORING:
90-100 = Excellent
75-89 = Strong
60-74 = Acceptable
40-59 = Weak
0-39 = Poor

Return scores from 0 to 100.
"""
)

class ExplanationJudge:

    def __init__(self):
        llm = get_llm()

        self.chain = (
            explanation_prompt
            | llm.with_structured_output(
                ExplanationEvaluation,
                method="json_schema",
                strict=True,
            )
        )

    def evaluate(
        self,
        resume,
        job_description,
        matched_skills,
        missing_skills,
        strengths,
        recommendations,
        reference_strengths,
        reference_recommendations,
    ):
        return self.chain.invoke(
            {
                "resume": resume,
                "job_description": job_description,
                "matched_skills": matched_skills,
                "missing_skills": missing_skills,
                "strengths": strengths,
                "recommendations": recommendations,
                "reference_strengths": reference_strengths,
                "reference_recommendations": reference_recommendations,
            }
        )
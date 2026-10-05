from langsmith import Client
from app.core.config import settings

from app.ai.analyzers.job_matcher import JobMatcher
from app.evaluation.evaluators import evaluate_skills, evaluate_score 
from app.evaluation.judges import  ExplanationJudge

from app.schemas.ai.job_match_analysis import JobMatchAnalysis
from app.schemas.ai.resume_analysis import ResumeAnalysis

judge = ExplanationJudge()
client = Client(
    api_url=settings.langsmith_endpoint,
    api_key=settings.langsmith_api_key,
)

DATASET_NAME = "career-copilot-job-matching"


def target(inputs: dict):
    matcher = JobMatcher()

    resume = ResumeAnalysis.model_validate(inputs["resume"])

    result = matcher.match(
        resume=resume,
        job_description=inputs["job_description"],
    )

    return result.model_dump()
def evaluator(inputs, outputs, reference_outputs):
    if not outputs:
        return [{
            "key": "skill_accuracy",
            "score": 0.0,
            "comment": "Target produced no output."
        }]

    output = JobMatchAnalysis.model_validate(outputs)
    reference = reference_outputs

    skill_result = evaluate_skills(
        output=output,
        reference=reference,
    )

    score_result = evaluate_score(
        output=output,
        reference=reference,
    )

    results = [
        {
            "key": "skill_accuracy",
            "score": skill_result["score"],
        },
        {
            "key": "matched_skill_accuracy",
            "score": skill_result["matched_skill_accuracy"],
        },
        {
            "key": "missing_skill_accuracy",
            "score": skill_result["missing_skill_accuracy"],
        },
        {
            "key": "score_accuracy",
            "score": score_result["score"],
        },
    ]

    if (
        "reference_strengths" in reference
        and "reference_recommendations" in reference
    ):
        try:
            judge_result = judge.evaluate(
                resume=inputs["resume"],
                job_description=inputs["job_description"],
                matched_skills=output.matched_skills,
                missing_skills=output.missing_skills,
                strengths=output.strengths,
                recommendations=output.recommendations,
                reference_strengths=reference["reference_strengths"],
                reference_recommendations=reference["reference_recommendations"],
            )

            results.extend([
                {
                    "key": "strengths_quality",
                    "score": judge_result.strengths_score / 100,
                },
                {
                    "key": "recommendations_quality",
                    "score": judge_result.recommendations_score / 100,
                },
            ])

        except Exception as e:
            results.extend([
                {
                    "key": "strengths_quality",
                    "score": 0.0,
                    "comment": f"Judge failed: {str(e)}",
                },
                {
                    "key": "recommendations_quality",
                    "score": 0.0,
                    "comment": f"Judge failed: {str(e)}",
                },
            ])

    return results

    # Only evaluate explanations when reference explanations exist.
    if (
        "reference_strengths" in reference
        and "reference_recommendations" in reference
    ):
        judge_result = judge.evaluate(
            resume=inputs["resume"],
            job_description=inputs["job_description"],
            matched_skills=output.matched_skills,
            missing_skills=output.missing_skills,
            strengths=output.strengths,
            recommendations=output.recommendations,
            reference_strengths=reference["reference_strengths"],
            reference_recommendations=reference["reference_recommendations"],
        )

        results.extend([
            {
                "key": "strengths_quality",
                "score": judge_result.strengths_score / 100,
            },
            {
                "key": "recommendations_quality",
                "score": judge_result.recommendations_score / 100,
            },
        ])

    return results
def main():
    dataset = client.create_dataset(
        dataset_name=DATASET_NAME,
        description="Evaluation dataset for AI Career Copilot job matching",
    )
    
    examples = [{'inputs': {'resume': {'summary': 'AI engineer with experience building LLM applications.',
                            'skills': ['Python', 'FastAPI', 'LangGraph', 'RAG', 'Docker'],
                            'experience': ['Built production LLM applications'],
                            'education': [],
                            'projects': ['AI Career Copilot']},
                 'job_description': '\n'
                                    '            We are looking for an AI Engineer with experience in\n'
                                    '            Python, FastAPI, LangGraph, RAG, and Docker.\n'
                                    '            '},
      "outputs": {
    "matched_skills": [
        "Python", "FastAPI", "LangGraph", "RAG", "Docker"
    ],
    "missing_skills": [],
    "reference_score": 95,
    "reference_strengths": [
        "Strong experience building production LLM applications",
        "Direct experience with Python, FastAPI, LangGraph, RAG, and Docker"
    ],
    "reference_recommendations": []
}},
     {'inputs': {'resume': {'summary': 'Data scientist experienced in building predictive models and '
                                       'analytics systems.',
                            'skills': ['Python',
                                       'Pandas',
                                       'NumPy',
                                       'Scikit-learn',
                                       'SQL',
                                       'Machine Learning'],
                            'experience': ['Built predictive models for business forecasting',
                                           'Developed SQL data pipelines and analytical dashboards'],
                            'education': ['BSc Statistics'],
                            'projects': ['Customer churn prediction system']},
                 'job_description': '\n'
                                    '            Data Scientist required with Python, Pandas, NumPy,\n'
                                    '            Scikit-learn, SQL, and Machine Learning experience.\n'
                                    '            '},
      'outputs': {'matched_skills': ['Python',
                                     'Pandas',
                                     'NumPy',
                                     'Scikit-learn',
                                     'SQL',
                                     'Machine Learning'],
                  'missing_skills': [],
                  'reference_score': 95}},
     {'inputs': {'resume': {'summary': 'Machine learning engineer experienced in model development and '
                                       'deployment.',
                            'skills': ['Python', 'PyTorch', 'Scikit-learn', 'Docker', 'SQL'],
                            'experience': ['Developed and deployed machine learning models'],
                            'education': ['MSc Computer Science'],
                            'projects': ['Computer vision classification system']},
                 'job_description': '\n'
                                    '            ML Engineer needed with Python, PyTorch, Docker,\n'
                                    '            Kubernetes, and MLflow experience.\n'
                                    '            '},
      'outputs': {'matched_skills': ['Python', 'PyTorch', 'Docker'],
                  'missing_skills': ['Kubernetes', 'MLflow'],
                  'reference_score': 70}},
#      {'inputs': {'resume': {'summary': 'Backend engineer experienced with Python APIs and databases.',
#                             'skills': ['Python', 'FastAPI', 'PostgreSQL', 'Docker', 'Git'],
#                             'experience': ['Built REST APIs using FastAPI',
#                                            'Developed PostgreSQL-backed services'],
#                             'education': [],
#                             'projects': ['Backend microservice platform']},
#                  'job_description': '\n'
#                                     '            Backend Engineer required with Python, FastAPI, '
#                                     'PostgreSQL,\n'
#                                     '            Docker, and Git. AWS experience is preferred but not '
#                                     'required.\n'
#                                     '            '},
#       "outputs": {
#     "matched_skills": [
#         "Python",
#         "RAG",
#         "LangChain",
#         "LLM applications",
#         "vector databases"
#     ],
#     "missing_skills": [],
#     "reference_score": 80,
#     "reference_strengths": [
#         "Demonstrates practical AI experience through RAG and LLM projects",
#         "Has hands-on experience with Python and LangChain"
#     ],
#     "reference_recommendations": [
#         "Gain professional production experience building AI systems"
#     ]
# },},
#      {'inputs': {'resume': {'summary': 'Software engineer transitioning into AI engineering.',
#                             'skills': ['Python', 'Java', 'SQL'],
#                             'experience': ['Developed enterprise Java applications'],
#                             'education': ['BSc Computer Science'],
#                             'projects': ['Built a RAG chatbot using Python, LangChain, and Chroma',
#                                          'Developed an LLM-powered document search application']},
#                  'job_description': '\n'
#                                     '            AI Engineer required with Python, RAG, LangChain,\n'
#                                     '            LLM applications, and vector databases.\n'
#                                     '            '},
#       'outputs': {'matched_skills': ['Python',
#                                      'RAG',
#                                      'LangChain',
#                                      'LLM applications',
#                                      'vector databases'],
#                   'missing_skills': [],
#                   'reference_score': 80}},
#      {'inputs': {'resume': {'summary': 'AI engineer experienced with modern LLM frameworks.',
#                             'skills': ['Python', 'LangChain', 'LlamaIndex', 'RAG', 'OpenAI API'],
#                             'experience': ['Built RAG applications using LlamaIndex'],
#                             'education': [],
#                             'projects': ['Enterprise document assistant']},
#                  'job_description': '\n'
#                                     '            AI Engineer required with Python, LangGraph,\n'
#                                     '            RAG, and OpenAI experience.\n'
#                                     '            '},
#       'outputs': {'matched_skills': ['Python', 'RAG', 'OpenAI'],
#                   'missing_skills': ['LangGraph'],
#                   'reference_score': 75}},
#      {'inputs': {'resume': {'summary': 'Frontend developer experienced in building web interfaces.',
#                             'skills': ['JavaScript', 'React', 'TypeScript', 'REST APIs'],
#                             'experience': ['Built React applications consuming REST APIs'],
#                             'education': [],
#                             'projects': ['React dashboard application']},
#                  'job_description': '\n'
#                                     '            AI Engineer required with Python, FastAPI, RAG,\n'
#                                     '            LangChain, and machine learning experience.\n'
#                                     '            '},
#       'outputs': {'matched_skills': [],
#                   'missing_skills': ['Python', 'FastAPI', 'RAG', 'LangChain', 'machine learning'],
#                   'reference_score': 10}},
#      {'inputs': {'resume': {'summary': 'Junior Python developer with machine learning projects.',
#                             'skills': ['Python', 'PyTorch', 'Machine Learning', 'Docker'],
#                             'experience': ['Completed academic machine learning projects'],
#                             'education': ['BSc Computer Science'],
#                             'projects': ['Image classification model', 'Recommendation system']},
#                  'job_description': '\n'
#                                     '            Senior Machine Learning Engineer required with '
#                                     'Python,\n'
#                                     '            PyTorch, Docker, Kubernetes, and 5+ years of '
#                                     'production ML experience.\n'
#                                     '            '},
#       "outputs": {
#     "matched_skills": [
#         "Python",
#         "PyTorch",
#         "Docker",
#         "Machine Learning"
#     ],
#     "missing_skills": [
#         "Kubernetes",
#         "5+ years production ML experience"
#     ],
#     "reference_score": 50,
#     "reference_strengths": [
#         "Strong foundation in Python and PyTorch",
#         "Has machine learning project experience"
#     ],
#     "reference_recommendations": [
#         "Gain production machine learning experience",
#         "Develop Kubernetes experience"
#     ]
# },},
#      {'inputs': {'resume': {'summary': 'Developer interested in AI.',
#                             'skills': ['Python', 'PyTorch', 'RAG', 'LangGraph'],
#                             'experience': [],
#                             'education': [],
#                             'projects': []},
#                  'job_description': '\n'
#                                     '            AI Engineer required with Python, PyTorch, RAG,\n'
#                                     '            and LangGraph experience building production '
#                                     'systems.\n'
#                                     '            '},
#       'outputs': {'matched_skills': ['Python', 'PyTorch', 'RAG', 'LangGraph'],
#                   'missing_skills': ['production AI experience'],
#                   'reference_score': 60}},
#      {'inputs': {'resume': {'summary': 'AI engineer building production LLM applications.',
#                             'skills': ['Python', 'FastAPI', 'LangGraph', 'RAG', 'Docker', 'PostgreSQL'],
#                             'experience': ['Built production RAG pipelines',
#                                            'Developed agentic AI applications'],
#                             'education': [],
#                             'projects': ['AI automation platform']},
#                  'job_description': '\n'
#                                     '            AI Engineer required with Python, RAG, LangGraph,\n'
#                                     '            Docker, and AWS experience.\n'
#                                     '            '},
#       'outputs': {'matched_skills': ['Python', 'RAG', 'LangGraph', 'Docker'],
#                   'missing_skills': ['AWS'],
#                   'reference_score': 85}}
]


    
    client.create_examples(
    inputs=[example["inputs"] for example in examples],
    outputs=[example["outputs"] for example in examples],
    dataset_id=dataset.id,
)

    results = client.evaluate(
        target,
        data=dataset,
        evaluators=[evaluator],
        experiment_prefix="job-matching-evaluation",
    )

    print(results)


if __name__ == "__main__":
    main()
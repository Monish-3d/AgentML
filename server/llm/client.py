from langchain_openai import ChatOpenAI
from llm.schema import Plan
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

health_model = ChatOpenAI(model="gpt-5.4-nano-2026-03-17")

plan_model = ChatOpenAI(model='gpt-5.4-mini-2026-03-17')
struct_model = plan_model.with_structured_output(Plan)

def get_preprocess_steps(prompt: str):
    """
    Calls the LLM with structured output and returns List[Preprocess_steps].
    Raises on failure — llm_recommend_node handles the exception.
    """
    response = struct_model.invoke(prompt)
    return response.steps


def get_health_explanation(report: dict) -> str:
    """
    Generates a plain-English explanation of the dataset health report.
    """
    prompt = f"""
    You are a friendly data analyst explaining dataset quality to a beginner.

    Given the following dataset health report, write a short and simple explanation (4-6 sentences).
    Mention the health score, any missing values, skewed columns, and key warnings.
    Avoid technical jargon. Be encouraging and constructive.

    HEALTH SCORE: {report['health_score']} / 100
    DATASET SUMMARY: {report['summary']}
    MISSING VALUES: {report['missing']}
    SKEWNESS: {report['skewness']}
    SCHEMA: {report['schema']}
    WARNINGS: {report['validation_warnings']}
    """
    try:
        response = health_model.invoke(prompt)
        return response.content
    except Exception as e:
        return f"Health explanation unavailable: {str(e)}"

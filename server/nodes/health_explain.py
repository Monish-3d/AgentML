from workflow.state import AgentMLState
from llm.client import get_health_explanation


def health_explain_node(state: AgentMLState) -> AgentMLState:

    report = {
        "summary": state.get("summary", {}),
        "missing": state.get("missing_json", {}),
        "skewness": state.get("skewness", {}),
        "health_score": state.get("health_score", 0),
        "schema": state.get("schema", {}),
        "validation_warnings": state.get("validation_warnings", []),
    }

    explanation = get_health_explanation(report)

    return {
        "health_explanation": explanation,
        "current_node": "health_explain",
        "progress": 93,
    }

from workflow.state import AgentMLState
from llm.client import get_preprocess_steps


def llm_recommend_node(state: AgentMLState) -> AgentMLState:

    try:
        steps = get_preprocess_steps(state["llm_prompt"])
        return {
            "recommended_steps": steps, "llm_error": None,
            "current_node": "llm_recommend", "progress": 65,
        }

    except Exception as e:
        return {
            "recommended_steps": [], "llm_error": str(e),
            "current_node": "llm_recommend", "progress": 65,
        }

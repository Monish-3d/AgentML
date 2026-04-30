from workflow.state import AgentMLState
from tools.encoding_tools import quick_encode

def quick_preprocess_node(state: AgentMLState) -> AgentMLState:

    if state.get("df") is None:
        return {
            "current_node": "quick_preprocess",
            "progress": 20,
            "quick_logs": ["Skipped — no valid DataFrame from ingest node."],
        }

    df, logs = quick_encode(state["df"])

    return {
        "df": df,
        "quick_logs": logs,
        "current_node": "quick_preprocess",
        "progress": 20,
    }

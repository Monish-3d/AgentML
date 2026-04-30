from workflow.state import AgentMLState
from tools.preprocessing_tools import apply_preprocessing

def apply_preprocessing_node(state: AgentMLState) -> AgentMLState:

    if state.get("df") is None:
        return {
            "current_node": "apply_preprocessing", "progress": 85, "apply_logs": ["Skipped — no valid DataFrame."]
        }

    df, logs = apply_preprocessing(df = state["df"], steps = state["validated_steps"], target = state["target"])

    return {"processed_df": df, "apply_logs": logs,"current_node": "apply_preprocessing", "progress": 85}

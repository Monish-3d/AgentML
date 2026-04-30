import os
from workflow.state import AgentMLState


def output_node(state: AgentMLState) -> AgentMLState:

    # Explicit None check - fix for "truth value of DataFrame is ambiguous" error
    processed = state.get("processed_df")
    df_to_save = processed if processed is not None else state.get("df")

    if df_to_save is None:
        return {
            "current_node": "output",
            "progress": 100,
            "output_path": "",
        }

    os.makedirs("outputs", exist_ok=True)
    output_path = os.path.join("outputs", f"{state['job_id']}.csv")
    df_to_save.to_csv(output_path, index=False)

    return {
        "output_path": output_path,
        "current_node": "output",
        "progress": 100,
    }

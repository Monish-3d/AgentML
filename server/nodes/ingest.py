import pandas as pd
from workflow.state import AgentMLState

def ingest_node(state: AgentMLState) -> AgentMLState:
    raw_df = state["raw_df"]
    filename = state["filename"]
    target = state["target"]
    errors = state.get("errors", [])

    if not isinstance(raw_df, pd.DataFrame):
        errors.append("Uploaded file could not be parsed into a valid DataFrame.")
        return {
            "errors": errors,
            "current_node": "ingest",
            "progress": 10,
        }

    if raw_df.empty:
        errors.append(f"'{filename}' is empty. Please upload a dataset.")
        return {
            "errors": errors,
            "current_node": "ingest",
            "progress": 10,
        }

    if raw_df.shape[1] < 2:
        errors.append(f"'{filename}' has only {raw_df.shape[1]} column(s). A valid dataset needs at least 2 columns.")
        return {
            "errors": errors,
            "current_node": "ingest",
            "progress": 10,
        }

    # warning only in this one
    if raw_df.shape[0] < 10:
        errors.append(f"Warning: '{filename}' has only {raw_df.shape[0]} rows. Results may be unreliable.")

    if target and target not in raw_df.columns:
        errors.append(f"Target column '{target}' not found in '{filename}'. Available columns: {list(raw_df.columns)}")
        return {
            "errors": errors,
            "current_node": "ingest",
            "progress": 10,
        }

    df = raw_df.copy()

    return { "df": df, "errors": errors, "current_node": "ingest", "progress": 10}

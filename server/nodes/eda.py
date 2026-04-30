import pandas as pd
from workflow.state import AgentMLState
from tools.eda_tools import dataset_summary, missing_values, statistics
from tools.distribution_tools import compute_skewness
from tools.correlation_tools import correlation_matrix
from tools.health_tools import compute_health_score


def eda_node(state: AgentMLState) -> AgentMLState:

    if state.get("df") is None:
        return {
            "current_node": "eda",
            "progress": 45,
        }

    df = state["df"]
    target = state["target"]
    problem_type = state["problem_type"]

    summary = dataset_summary(df)
    missing = missing_values(df)
    stats = statistics(df)
    skewness = compute_skewness(df)

    # Correlation fix — round first, then convert to plain Python floats via JSON round-trip
    corr = correlation_matrix(df)
    if corr is not None:
        correlation_json = {
            col: {k: round(float(v), 4) for k, v in row.items()}
            for col, row in corr.to_dict().items()
        }
    else:
        correlation_json = None

    # Imbalance - use only for classification 
    imbalance_ratio = None
    if problem_type == "classification" and target in df.columns:
        value_counts = df[target].value_counts()
        if len(value_counts) >= 2:
            imbalance_ratio = round(float(value_counts.iloc[0] / value_counts.iloc[-1]), 2)

    health_score = compute_health_score(df, skewness, imbalance_ratio)

    return {
        "summary": summary,
        "missing_json": missing,
        "stats_json": stats,
        "skewness": skewness,
        "correlation_json": correlation_json,
        "imbalance_ratio": imbalance_ratio,
        "health_score": health_score,
        "current_node": "eda",
        "progress": 45,
    }

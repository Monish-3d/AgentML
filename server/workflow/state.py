from typing import TypedDict, Any, Optional

class AgentMLState(TypedDict):
    raw_df: Any          # pd.DataFrame — execution only
    df: Any              # pd.DataFrame — execution only
    processed_df: Any    # pd.DataFrame — execution only

    # ── Everything else is JSON-safe and forms the API response
    job_id: str
    target: str
    problem_type: str
    filename: str
    current_node: str    # for progress tracking
    progress: int        # 0-100

    quick_logs: list[str]
    schema: dict
    summary: dict
    stats_json: dict         # df.describe().to_dict() — serializable
    missing_json: dict       # df.isnull().sum().to_dict()
    skewness: dict
    correlation_json: Optional[dict]  # corr.to_dict() if not None
    imbalance_ratio: Optional[float]
    health_score: int

    llm_prompt: str
    recommended_steps: list[dict]   # serialized step dicts, not Pydantic objects
    llm_error: Optional[str]
    validated_steps: list[dict]
    validation_warnings: list[str]
    apply_logs: list[str]

    health_explanation: str
    output_path: str        # path to saved CSV on disk
    errors: list[str]
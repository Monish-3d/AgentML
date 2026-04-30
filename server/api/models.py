from pydantic import BaseModel
from typing import Optional


class RunRequest(BaseModel):
    target: str
    problem_type: str

class JobStartResponse(BaseModel):
    job_id: str
    message: str


class JobStatusResponse(BaseModel):
    job_id: str
    status: str
    current_node: str
    progress: int
    error: Optional[str] = None    # for troubleshooting


class JobResultResponse(BaseModel):
    job_id: str
    status: str
    summary: dict
    dataset_schema: dict
    missing: dict
    stats: dict
    skewness: dict
    correlation: Optional[dict]
    imbalance_ratio: Optional[float]
    health_score: int
    health_explanation: str
    quick_logs: list
    recommended_steps: list
    validated_steps: list
    validation_warnings: list
    apply_logs: list
    errors: list
    download_url: str

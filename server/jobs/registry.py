import uuid
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class JobRecord:
    job_id: str
    filename: str
    status: str = "pending"       # pending | running | completed | failed
    current_node: str = ""
    progress: int = 0
    output_path: str = ""
    error: Optional[str] = None
    result: dict = field(default_factory=dict)


# Simple in-memory store- one dic for the lifetime of the server process
_store: dict[str, JobRecord] = {}


def create_job(filename: str) -> str:
    job_id = str(uuid.uuid4())
    _store[job_id] = JobRecord(job_id=job_id, filename=filename)
    return job_id


def get_job(job_id: str) -> Optional[JobRecord]:
    return _store.get(job_id)


def update_job(job_id: str, **kwargs):
    job = _store.get(job_id)
    if job:
        for key, value in kwargs.items():
            setattr(job, key, value)

from fastapi import HTTPException
from jobs.registry import get_job, JobRecord

def get_job_or_404(job_id: str) -> JobRecord:
    """Shared dependency - fetches a job or raises 404"""
    job = get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail=f"Job '{job_id}' not found.")
    return job

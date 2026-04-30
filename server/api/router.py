import os
from fastapi import APIRouter, UploadFile, File, Form, BackgroundTasks, Depends
from fastapi.responses import FileResponse
from fastapi.exceptions import HTTPException

from api.models import JobStartResponse, JobStatusResponse, JobResultResponse
from api.dependencies import get_job_or_404
from jobs.registry import create_job, JobRecord
from jobs.runner import execute_graph

router = APIRouter()
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/run", response_model=JobStartResponse)
async def run_pipeline(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    target: str = Form(...),
    problem_type: str = Form(...),
):
    if not file.filename.endswith((".csv", ".xlsx")):
        raise HTTPException(status_code=400, detail="Only .csv and .xlsx files are supported.")

    job_id = create_job(file.filename)
    file_path = os.path.join(UPLOAD_DIR, f"{job_id}_{file.filename}")
    with open(file_path, "wb") as f:
        f.write(await file.read())

    background_tasks.add_task(
        execute_graph, job_id, file_path, target, problem_type, file.filename
    )

    return JobStartResponse(job_id=job_id, message="Pipeline started successfully.")


@router.get("/status/{job_id}", response_model=JobStatusResponse)
def get_status(job: JobRecord = Depends(get_job_or_404)):
    return JobStatusResponse(
        job_id=job.job_id,
        status=job.status,
        current_node=job.current_node,
        progress=job.progress,
        error=job.error
    )


@router.get("/result/{job_id}", response_model=JobResultResponse)
def get_result(job: JobRecord = Depends(get_job_or_404)):
    if job.status != "completed":
        raise HTTPException(status_code=202, detail=f"Job not complete yet. Status: '{job.status}'.")

    return JobResultResponse(
        job_id=job.job_id, status=job.status,
        download_url=f"/api/v1/download/{job.job_id}",
        **job.result
    )


@router.get("/download/{job_id}")
def download_result(job: JobRecord = Depends(get_job_or_404)):
    if job.status != "completed":
        raise HTTPException(status_code=202, detail="Job is not complete yet.")

    if not job.output_path or not os.path.exists(job.output_path):
        raise HTTPException(status_code=404, detail="Output file not found.")

    return FileResponse(
        path=job.output_path, media_type="text/csv",
        filename=f"processed_{job.filename}"
    )

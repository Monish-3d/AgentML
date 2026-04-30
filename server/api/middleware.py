import time
import logging
from fastapi import Request

logger = logging.getLogger("agentML")


async def log_requests(request: Request, call_next):
    """Logs method, path, and response time for every request."""
    start = time.time()
    response = await call_next(request)
    duration = round(time.time() - start, 3)
    logger.info(f"{request.method} {request.url.path} — {response.status_code} ({duration}s)")
    return response

import time 
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logging.basicConfig(level= logging.INFO)
logger = logging.getLogger("app")

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.time()
        response = await call_next(request)
        duration =  time.time()-start_time
        logger.info(
                  f"{request.method} {request.url.path}"
            f"->{response.status_code} ({duration:.4f}s)"
        )
        response.headers["X-Process-Time"] = f"{duration:.4f}"
        return response

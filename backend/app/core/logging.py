"""
Application Logging Configuration.
"""

import logging
import sys
import time
from functools import wraps

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(name)s]: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("ai_farmer_advisory")

def log_execution_time(action_name: str):
    """Decorator to log execution latency of services and API endpoints."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            try:
                result = func(*args, **kwargs)
                duration = time.perf_counter() - start
                logger.info(f"[PERF] {action_name} completed in {duration:.3f}s")
                return result
            except Exception as e:
                duration = time.perf_counter() - start
                logger.error(f"[PERF] {action_name} failed after {duration:.3f}s: {e}")
                raise
        return wrapper
    return decorator


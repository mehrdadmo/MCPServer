# Add caching
from functools import lru_cache

@lru_cache(maxsize=100)
def cache_common_queries(prompt, context_hash):
    # Implement caching logic
    pass

# Add logging
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add authentication
from fastapi import Security, Depends
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key")

def get_api_key(api_key: str = Depends(api_key_header)):
    if api_key != os.getenv("API_KEY"):
        raise HTTPException(status_code=403)
    return api_key 
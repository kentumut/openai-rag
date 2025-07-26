from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from slowapi.middleware import SlowAPIMiddleware
from settings import settings
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from qdrant_client import QdrantClient
from query import router as query_router

# Collapse all middleware…
middleware = [
    Middleware(SlowAPIMiddleware),
    Middleware(CORSMiddleware, **settings.cors),
]

app = FastAPI(
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
    middleware=middleware,
)

# Rate‑limit boilerplate
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Qdrant client on app.state
app.state.qdrant_client = QdrantClient(path=settings.qdrant_path)

# Routes
app.include_router(query_router)

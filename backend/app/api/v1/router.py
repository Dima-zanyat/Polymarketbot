from fastapi import APIRouter

from app.api.v1.endpoints import health
from app.api.v1.endpoints import leaderboards_stats

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(leaderboards_stats.router)

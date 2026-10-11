
from fastapi import FastAPI
from contextlib import asynccontextmanager

import httpx

from app.core.logging import setup_logging, get_logger
from app.config import settings
from app.api.v1.router import api_router

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Управление ресурсами на старте."""
    setup_logging()
    logger.info("Запуск %s , %s", settings.app_name, settings.envrioment)
    logger.info("Тут будут каки-то метрики по боту")
    app.state.client = httpx.AsyncClient()
    try:
        yield
    finally:
        await app.state.client.aclose()
    logger.info("Приложение остановлено.")


def create_app() -> FastAPI:
    """Сборищик приложений."""

    is_prod = None
    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        debug=settings.debug,
        lifespan=lifespan,
        docs_url=None if is_prod else "/docs",
        redoc_url=None if is_prod else "/redoc",
        openapi_url=None if is_prod else "/openapi.json",
    )
    app.include_router(api_router, prefix=settings.api_v1_prefix)

    return app


app = create_app()

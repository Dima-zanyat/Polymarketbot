from typing import Any
import logging

from httpx import AsyncClient
from requests import Response

from app.schemas.leaderboards import LeadeboardsResponseSchema
from app.schemas.stats import StatSchema
from app.schemas.position import PositionSchema

logger = logging.getLogger(__name__)


class PolymarketStatsService:
    """Получение ститистики лидеров."""

    BASE_URL = "https://data-api.polymarket.com/"

    def __init__(self, client: AsyncClient) -> None:
        """"""
        self._client = client

    async def _get(
        self,
        path: str,
        *,
        params: dict[str, Any],
    ):
        """Общий запросник."""
        response = await self._client.get(f"{self.BASE_URL}{path}", params=params)
        response.raise_for_status()
        return response.json()

    async def get_leaderboards(
        self,
        limit: int,
        time_period: str,
    ) -> list[LeadeboardsResponseSchema]:
        """Получает таблицу лидеров."""
        response = await self._client.get(
            f"{self.BASE_URL}v2/leaderboard",
            params={
                "limit": limit,
                "time_period": time_period,
            },
        )
        response.raise_for_status()
        if isinstance(response, BaseException):
            logger.info("ошибка %s", response)
        return [
            LeadeboardsResponseSchema.model_validate(user)
            for user in response.json().get("data")
        ]

    @staticmethod
    def dict_in_shemas(response: dict):
        positions = [PositionSchema.model_validate(pos) for pos in response["data"]]
        return positions

    async def get_user_stat(self, wallet: str) -> StatSchema:
        """Детальная информация по каждому пользователю."""
        response = await self._get("v2/user-stats", params={"user": wallet})
        return StatSchema.model_validate(response["data"])

    async def get_position(
        self, wallet: str, *, limit: int = 100
    ) -> list[PositionSchema]:
        """Где и на какие суммы торгует пользователь."""
        # Закрытые позиции трейдера
        response_closed = await self._get(
            "v2/positions", params={"user": wallet, "limit": limit, "status": "closed"}
        )
        # Открытые позиции трейдера
        response = await self._get(
            "v2/positions",
            params={
                "user": wallet,
                "limit": limit,
            },
        )
        positions = self.dict_in_shemas(response)
        positions.extend(self.dict_in_shemas(response_closed))
        return positions

    async def get_activity(
        self, wallet: str, *, limit: int = 100
    ) -> dict[str, Any] | list[dict[str, Any]]:
        """Buy, sell, redeem и временная последовательность."""
        return await self._get("v2/activity", params={"user": wallet, "limit": limit})

    async def get_trade(
        self, wallet: str, *, limit: int = 100
    ) -> dict[str, Any] | list[dict[str, Any]]:
        """Реалльные трейды для анализа стратегии."""
        return await self._get("v2/trades", params={"user": wallet, "limit": limit})

    async def get_user_pnl(self, wallet) -> dict[str, Any] | list[dict[str, Any]]:
        """Стаблильность прибыли и drawdown."""
        return await self._get("v2/user-pnl", params={"user": wallet})

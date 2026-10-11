import asyncio
import logging

from app.services.polymarket_data import PolymarketStatsService
from app.selectors.selectors import Selectors
from app.schemas.leaderboards import LeadeboardsResponseSchema
from app.schemas.position import PositionSchemaSelector
from app.selectors.view_traders import load_wallet

logger = logging.getLogger(__name__)

MAX_CONCURNCY: int = 3


class CollectLeaderboardsService:
    """Собирает информация о пользователях."""

    def __init__(self, polymarket) -> None:
        self._polymarket: PolymarketStatsService = polymarket
        self._semaphore = asyncio.Semaphore(MAX_CONCURNCY)
        self._selectors = Selectors()
        self.select_traders: list = []
        self.view_traders = load_wallet()

    async def collected_stats_traders(
        self,
        limit: int,
        time_period: str,
    ) -> list[str]:
        """Объединяет полученную информацию в один ответ."""

        leaderboards = await self._polymarket.get_leaderboards(
            limit=limit,
            time_period=time_period,
        )
        tasks = [self._collect_one(trader) for trader in leaderboards]

        await asyncio.gather(*tasks, return_exceptions=True)

        return self.select_traders

    async def _collect_one(self, trader: LeadeboardsResponseSchema):
        wallet = trader.proxy_wallet
        async with self._semaphore:
            (
                stats,
                position,
                activity,
                trade,
                user_pnl,
            ) = await asyncio.gather(
                self._polymarket.get_user_stat(wallet),
                self._polymarket.get_position(wallet, limit=100),
                self._polymarket.get_activity(wallet, limit=100),
                self._polymarket.get_trade(wallet, limit=100),
                self._polymarket.get_user_pnl(wallet),
            )
        all_positinon_selector = 0
        win_positions_selector = 0
        for pos in position:
            all_positinon_selector += 1
            if pos.current_price == 1:
                win_positions_selector += 1
        position_selector = PositionSchemaSelector(
            count_closed_position=all_positinon_selector,
            win_position=win_positions_selector,
        )
        if (
            await self._selectors.stats.run(stats)
            and await self._selectors.position.run(position_selector)
            and await self._selectors.view_traders.run(self.view_traders, wallet)
        ):

            self.select_traders.append(wallet)

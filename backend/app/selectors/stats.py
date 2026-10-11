from decimal import Decimal

from app.schemas.stats import StatSchema

MIN_TRADES: int = 5
MAX_TRADED_MARKETS: int = 20000
MIN_PNL_VOLUME: Decimal = Decimal("5000")


class StatsSelector:

    async def run(self, stats: StatSchema):
        return all(
            [
                await self._range_trades(stats),
                await self._pnl_volume(stats),
            ]
        )

    async def _range_trades(
        self,
        stats: StatSchema,
    ) -> bool:
        return MIN_TRADES < stats.trades < MAX_TRADED_MARKETS

    async def _pnl_volume(self, stats: StatSchema) -> bool:
        return stats.all_time_pnl.trade_pnl >= MIN_PNL_VOLUME

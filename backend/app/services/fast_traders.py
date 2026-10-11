from app.services.polymarket_data import PolymarketStatsService


class FastTradersService:

    def __init__(self, polymarket) -> None:
        self._polymarket: PolymarketStatsService = polymarket
        self._semaphore = asyncio.Semaphore(MAX_CONCURNCY)
        self._selectors = Selectors()
        self.select_traders: list = []
        self.view_traders = load_wallet()

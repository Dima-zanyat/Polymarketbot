import json

from pathlib import Path

FILE_PATH = Path("E:/Dev/polymarket_bot_analyze/backend/app/data/see_traders.json")


def load_wallet() -> list[str | None]:
    """Загружает данные о просмотренных кошельках."""
    if not FILE_PATH.exists():
        return list()
    try:
        with open(FILE_PATH, "r") as file:
            data = json.load(file)
    except json.JSONDecodeError:
        return list()
    return data["wallets"]


class ViewTradersSelector:

    def __init__(self) -> None:
        self._file_path: Path = FILE_PATH

    async def run(self, trader_walets: list[str | None], trader: str):
        return await self._trader_in_view_traders(
            trader_walets=trader_walets, trader=trader
        )

    async def _trader_in_view_traders(
        self, trader_walets: list[str | None], trader: str
    ) -> bool:
        if trader not in trader_walets:
            return True
        return False

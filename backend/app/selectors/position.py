from app.schemas.position import PositionSchemaSelector

WINRATE: int = 70


class PositionSelector:

    async def run(self, position_selector: PositionSchemaSelector):
        return await self._validate_winrate(
            position_selector.count_closed_position,
            position_selector.win_position,
        )

    async def _calculate_winrate(
        self, count_closed_position: int, win_position: int
    ) -> float:
        """Подсчет винрейта."""
        if count_closed_position == 0:
            return 0
        winrate = (win_position / count_closed_position) * 100
        return winrate

    async def _validate_winrate(
        self, count_closed_position: int, win_position: int
    ) -> bool:
        """Проверка допуска по винрейту."""

        if (
            await self._calculate_winrate(count_closed_position, win_position)
            >= WINRATE
        ):
            return True
        return False

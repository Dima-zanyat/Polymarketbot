from app.selectors.stats import StatsSelector
from app.selectors.position import PositionSelector
from app.selectors.view_traders import ViewTradersSelector


class Selectors:
    def __init__(self) -> None:
        self.stats = StatsSelector()
        self.position = PositionSelector()
        self.view_traders = ViewTradersSelector()

"""Схема для запроса https://data-api.polymarket.com/v2/positions."""

from decimal import Decimal

from pydantic import BaseModel


class PositionSchema(BaseModel):

    condition_id: str
    current_price: Decimal  # Текущая цена
    total_pnl: Decimal  # Общий PnL, указанный API
    percent_pnl: Decimal


class PositionSchemaSelector(BaseModel):

    count_closed_position: int
    win_position: int

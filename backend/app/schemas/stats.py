from decimal import Decimal

from pydantic import BaseModel


class AllTimePnlSchema(BaseModel):
    trade_pnl: Decimal  # прибыль/убыток
    volume_usdc: Decimal  # Общий объем


class StatSchema(BaseModel):
    trades: int  # Количество уникальных рынков
    all_time_pnl: AllTimePnlSchema

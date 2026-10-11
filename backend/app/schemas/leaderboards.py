from decimal import Decimal

from pydantic import BaseModel


class LeadeboardsResponseSchema(BaseModel):

    rank: int
    user_id: str
    pnl: Decimal
    volume: Decimal
    user_name: str

    @property
    def proxy_wallet(self):
        return self.user_id.lower()

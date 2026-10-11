from typing import Annotated

import httpx

from fastapi import Request, Depends

from app.services.polymarket_data import PolymarketStatsService
from app.services.collect_traders import CollectLeaderboardsService
from app.services.build_message import build_message


def get_client(request: Request):
    return request.app.state.client


def get_leaderboards_service(client: httpx.AsyncClient = Depends(get_client)):
    return PolymarketStatsService(client)


def get_collected_leaderboards_stats_service(
    polymarket: PolymarketStatsService = Depends(get_leaderboards_service),
):
    return CollectLeaderboardsService(polymarket)


DepLeaderboardsStatsService = Annotated[
    CollectLeaderboardsService, Depends(get_collected_leaderboards_stats_service)
]


get_build_message = build_message

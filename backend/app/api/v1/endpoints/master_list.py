+from enum import Enum

from fastapi import APIRouter, Query

from app.dependecies.leaderboards_stats import (
    DepLeaderboardsStatsService,
    get_build_message,
)

router = APIRouter(tags=["master_list"])


class Period(str, Enum):
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    ALL = "all"


@router.get(
    "/master-list",
    summary="Получаем данные по пользователям",
    response_model=dict[str, list[str]],
)
async def get_leaderbords(
    service: DepLeaderboardsStatsService,
    limit: int = Query(default=20, ge=1, le=1000),
    time_period: str = Query(
        default=Period.MONTH,
        description="Временная метка.",
    ),
):
    wallets = await service.collected_stats_traders(
        limit=limit, time_period=time_period
    )
    profiles_users = get_build_message(wallets=wallets)
    return {
        "wallets": wallets,
        "profile_url": profiles_users,
    }

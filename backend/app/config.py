"""Настройки приложения."""

from typing import Literal


class Settings:
    """"""

    app_name: str = "Polymarket Bot"

    log_level: str = "INFO"
    db_echo: bool = False

    envrioment: Literal["prod", "test"] = "test"

    debug: bool = True

    # api
    api_v1_prefix: str = "/api/v1"


settings = Settings()

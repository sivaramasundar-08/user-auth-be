import logging
from functools import lru_cache
from typing import Any, Dict, List

from pydantic_settings import BaseSettings

from app.config.constants import Constants
from app.utils.logger import logger


class AppConfig(BaseSettings):
    database_url: str
    db_name: str
    db_username: str
    db_password: str
    secret_key: str
    algorithm: str

    class Config:
        env_file = ".env"
        validate_assignment = True


app_config = AppConfig()

from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    Uses python-dotenv to load secret keys from .env file in
    root directory
    """

    API_KEY: str
    EXCHANGE_URL: str
    HISTORICAL_URL: str
    SECRET: str
    ALGORITHM: str

    class Config:
        env_file = ".env"


# Reading from the file system is costly. The @lru_cache helps us load
# The .env file only once
@lru_cache()
def get_settings():
    return Settings()

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
    ACCESS_TOKEN: str
    OPEN_API_HISTORICAL: str
    OPEN_API_RATES: str

    class Config:
        env_file = ".env"


# Reading from the file system is costly. The @lru_cache helps us load
# The .env file only once
@lru_cache()
def get_settings():
    return Settings()

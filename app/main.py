import logging

from fastapi import FastAPI

from app.cache.redis import redis_cache

from app.db.database import Base, engine
from app.router import convert, historical_data, supported_currencies, users

# Setup logging
logger = logging.getLogger(__name__)
format = "%(asctime)s : %(name)s:%(lineno)d : %(levelname)s : %(message)s"
logging.basicConfig(
    format=format,
    level=logging.DEBUG,
    datefmt="%H:%M:%S",
    handlers=[logging.FileHandler("server_logs.log"), logging.StreamHandler()],
)


# Create fastapi instance
app = FastAPI()


# Load endpoints into fastapi app
app.include_router(convert.router)
app.include_router(historical_data.router)
app.include_router(supported_currencies.router)
app.include_router(users.router)


@app.on_event("startup")
async def startup_event():
    """Code to run during startup"""

    # Create database tables. We are going with this approach
    # for simplicity and brevity's sake. In a real-world scenario,
    # We'd be using Alembic to create tables and manage migrations.
    Base.metadata.create_all(bind=engine)

    # Start pool of connections to the Redis cache
    await redis_cache.start()


@app.on_event("shutdown")
async def shutdown_event():
    """Code to run during shutdown"""
    await redis_cache.close()
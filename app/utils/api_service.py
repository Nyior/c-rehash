import logging

import aiohttp

from app.config.settings import Settings


async def currency_api_caller(
    settings: Settings, url: str, headers: dict = None, params: dict = None
):
    """
    A helper function for calling the external APIs
    Moved the api-calling code to this separate function to separate concerns

    Args:
    * settings (Settings):
    * url (str): URL to external service
    * params (dict): query params
    """
    # headers = {"x-rapidapi-key": settings.API_KEY}

    try:
        logging.info(f"Request to {url} initiated.")
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as response:
                if response.content_type == "text/plain":
                    response = await response.text()
                else:
                    response = await response.json()

                logging.info(f"Request to {url} completed.")
                return response

    except Exception as e:
        error = f"erro: {e}"

        logging.exception(error)

        response = {"error": error}
        return response

from fastapi import Depends, APIRouter

from app.services.historical_data import historical_data_service
from app.schemas.historical_data import HistoricalData, HistoricalDataResponse
from app.config.settings import Settings, get_settings
from app.auth.auth_bearer import JWTBearer


router: APIRouter = APIRouter(prefix="/api/v1", dependencies=[Depends(JWTBearer())])


@router.post("/historical-data", response_model=HistoricalDataResponse)
async def historical_data(
    request_data: HistoricalData,
    settings: Settings = Depends(get_settings),
) -> HistoricalDataResponse:
    """
    Returns the exchange rate at the given date

    Args:
    * from_currency (str): base currency code
    * to (str): target currency code
    * date (str): date.
    * settings (Settings): houses env vars and external URLs
    """

    # The service function does all the heavy lifting
    response = await historical_data_service(
        request_data.from_currency,
        request_data.to_currency,
        request_data.date,
        settings,
    )

    return response

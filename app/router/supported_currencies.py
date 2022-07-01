from fastapi import APIRouter, Depends

from app.services.supported_currencies import supported_currencies_service
from app.auth.auth_bearer import JWTBearer


router: APIRouter = APIRouter(prefix="/api/v1", dependencies=[Depends(JWTBearer())])


@router.get("/supported-currencies")
def currencies():
    """
    Returns a list of all the currencies supported by this service
    """
    currencies = supported_currencies_service()
    return currencies

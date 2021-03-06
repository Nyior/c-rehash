from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.user import UserLoginSchema, UserSchema
from app.services.users import create_user_service, user_login_service

router: APIRouter = APIRouter(prefix="/api/v1/user")


@router.post("/signup")
async def create_user(user: UserSchema = Body(...), db: Session = Depends(get_db)):
    """
    Signup route.

    Args:
    * email (EmailStr): valid email
    * password (str):

    Returns:
    * response (dict): contains the generated access code.
    """
    response = await create_user_service(user=user, db=db)
    # users.append(user) # replace with db call, making sure to hash the password first
    return response


@router.post("/login")
async def user_login(user: UserLoginSchema = Body(...), db: Session = Depends(get_db)):
    """
    Login route handler.

    Args:
    * email (EmailStr): valid email
    * password (str):

    Returns:
    * response (dict): contains the generated access code.
    """
    response = await user_login_service(user=user, db=db)
    return response

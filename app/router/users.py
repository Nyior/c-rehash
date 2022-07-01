from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session

from app.schemas.user import UserSchema, UserLoginSchema
from app.services.users import create_user_service, user_login_service
from app.db.database import get_db


router: APIRouter = APIRouter(prefix="/api/v1/user")


@router.post("/signup")
def create_user(user: UserSchema = Body(...), db: Session = Depends(get_db)):
    """
    Signup route.

    Args:
    * email (EmailStr): valid email
    * password (str):

    Returns:
    * response (dict): contains the generated access code.
    """
    response = create_user_service(user=user, db=db)
    # users.append(user) # replace with db call, making sure to hash the password first
    return response


@router.post("/login")
def user_login(user: UserLoginSchema = Body(...), db: Session = Depends(get_db)):
    """
    Login route handler.

    Args:
    * email (EmailStr): valid email
    * password (str):

    Returns:
    * response (dict): contains the generated access code.
    """
    response = user_login_service(user=user, db=db)
    return response

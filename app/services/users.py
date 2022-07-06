import logging

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.auth.auth_handler import signJWT
from app.db.crud import (create_user, get_user_by_email,
                         validate_credentials)
from app.schemas.user import UserSchema


def create_user_service(user: UserSchema, db: Session):
    """
    Service for use in the signup route handler.

    Service functions foster Single Responsibility and Reusability.

    Args:
    * email (EmailStr): valid email
    * password (str):

    Raises:
    * HTTPException

    Returns:
    * response (dict): contains the generated access code.
    """
    db_user = get_user_by_email(db, email=user.email)
    if db_user is not None:
        message = f"Email, {user.email}, already registered"
        logging.exception(message)
        raise HTTPException(status_code=400, detail=message)
    user = create_user(db=db, user=user)

    response: dict = signJWT(user.email)
    return response


def user_login_service(user: UserSchema, db: Session):
    """
    Service for use in the login route handler.

    Service functions foster Single Responsibility and Reusability.

    Args:
    * email (EmailStr): valid email
    * password (str):

    Returns:
    * response (dict): contains the generated access code.
    """
    if validate_credentials(db, email=user.email, password=user.password):
        response: dict = signJWT(user.email)
        return response
    else:
        response: dict = {"error": "Invalid credentials"}
        return response

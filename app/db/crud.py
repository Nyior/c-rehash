"""
    Reusable functions for reading data from the database
"""
import bcrypt
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserSchema


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_user_by_email_password(db: Session, email: str, password: str):
    return (
        db.query(User)
        .filter(User.email == email and bcrypt.checkpw(password, User.hashed_password))
        .first()
    )


def create_user(db: Session, user: UserSchema):
    # Hash password before saving to database
    hashed_password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    email: EmailStr
    password: str

    class Config:
        schema_extra = {
            "example": {"email": "nyior@x.com", "password": "sample-password"}
        }


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

    class Config:
        schema_extra = {
            "example": {"email": "nyior@x.com", "password": "sample-password"}
        }

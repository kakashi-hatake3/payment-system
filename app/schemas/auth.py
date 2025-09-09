from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None
    user_type: str | None = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str

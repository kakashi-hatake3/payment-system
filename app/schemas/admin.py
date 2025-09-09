from pydantic import BaseModel, EmailStr


class AdminBase(BaseModel):
    email: EmailStr
    full_name: str


class AdminCreate(AdminBase):
    password: str


class AdminResponse(AdminBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

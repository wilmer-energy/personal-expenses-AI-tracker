from pydantic import BaseModel, EmailStr, Field


class CreateUser(BaseModel):
    name: str = Field(...)
    email: EmailStr
    password: str = Field(...)

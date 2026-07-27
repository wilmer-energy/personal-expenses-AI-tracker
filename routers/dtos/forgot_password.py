from pydantic import BaseModel, EmailStr


class ForgotPasswordDto(BaseModel):
    email: EmailStr
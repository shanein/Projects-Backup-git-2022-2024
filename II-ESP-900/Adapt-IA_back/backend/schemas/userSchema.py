from pydantic import BaseModel, EmailStr, UUID4
from typing import Optional
from datetime import date
from enum import Enum


class UserBase(BaseModel):
    email: EmailStr
    firstname: str
    lastname: str
    birthdate: date
    phone_number: str
    is_active: bool = True
    is_superuser: bool = False
    user_type: str
    last_login: Optional[date] = None
    company_name: str


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    firstname: str
    lastname: str
    birthdate: date
    phone_number: str
    user_type: str
    company_name: str


class UserUpdate(BaseModel):
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    phone_number: Optional[str] = None


class ShowUser(UserBase):
    id: UUID4

    class Config:
        from_attributes = True
        json_encoders = {
            date: lambda v: v.isoformat(),
        }

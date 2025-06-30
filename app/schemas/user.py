from uuid import UUID
from pydantic import BaseModel, EmailStr, Field
from typing import Optional


# ─────────────── Base Schema ───────────────
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    phone_number: Optional[str] = None  # <-- Add this line


# ─────────────── Input Schemas ───────────────
class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None  


class ChangePasswordRequest(BaseModel):
    current_password: str = Field(..., min_length=6)
    new_password: str = Field(..., min_length=6)


# ─────────────── Output Schemas ───────────────
class UserRead(UserBase):
    id: UUID
    is_active: bool

    class Config:
        from_attributes = True


class UserProfile(UserBase):
    id: UUID

    class Config:
        from_attributes = True


class UserOut(BaseModel):
    id: UUID
    full_name: Optional[str] = None
    email: EmailStr
    phone_number: Optional[str] = None  # <-- Add this line

    class Config:
        from_attributes = True

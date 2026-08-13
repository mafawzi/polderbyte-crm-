from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


# ---------- Users ----------
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str = "rep"


class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ---------- Companies ----------
class CompanyCreate(BaseModel):
    name: str
    industry: Optional[str] = None
    website: Optional[str] = None


class CompanyOut(CompanyCreate):
    id: int

    class Config:
        from_attributes = True


# ---------- Contacts ----------
class ContactCreate(BaseModel):
    company_id: Optional[int] = None
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    title: Optional[str] = None


class ContactOut(ContactCreate):
    id: int
    owner_id: Optional[int] = None

    class Config:
        from_attributes = True


# ---------- Deals ----------
class DealCreate(BaseModel):
    contact_id: Optional[int] = None
    company_id: Optional[int] = None
    title: str
    value: float = 0
    stage: str = "lead"


class DealUpdate(BaseModel):
    title: Optional[str] = None
    value: Optional[float] = None
    stage: Optional[str] = None


class DealOut(BaseModel):
    id: int
    contact_id: Optional[int]
    company_id: Optional[int]
    owner_id: Optional[int]
    title: str
    value: float
    stage: str
    created_at: datetime

    class Config:
        from_attributes = True


# ---------- Activities ----------
class ActivityCreate(BaseModel):
    deal_id: int
    type: str  # call|email|meeting|note
    content: str


class ActivityOut(BaseModel):
    id: int
    deal_id: int
    type: str
    content: str
    ai_summary: Optional[str] = None
    created_by: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


# ---------- Qualifications ----------
class QualificationOut(BaseModel):
    id: int
    deal_id: int
    criterion: str
    confirmed: bool
    notes: Optional[str] = None
    score: int
    assessed_at: datetime

    class Config:
        from_attributes = True

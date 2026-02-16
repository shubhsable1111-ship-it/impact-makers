from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import List, Optional, Annotated
from datetime import datetime
from bson import ObjectId


def validate_object_id(value: str) -> str:
    """Validate and convert ObjectId"""
    if not ObjectId.is_valid(value):
        raise ValueError("Invalid ObjectId")
    return value


# Type alias for ObjectId string
ObjectIdStr = Annotated[str, Field(..., json_schema_extra={"example": "507f1f77bcf86cd799439011"})]


class UserModel(BaseModel):
    """User model for MongoDB"""
    id: Optional[str] = Field(None, alias="_id")
    name: str
    email: EmailStr
    job_type: str
    months_active: int
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class CreditProfileModel(BaseModel):
    """Credit profile model for MongoDB"""
    id: Optional[str] = Field(None, alias="_id")
    user_id: str
    avg_income: float
    income_variance: float
    upi_txn_count: int
    bill_payment_score: int
    withdrawal_ratio: float
    digital_trust_score: int
    risk_category: str
    explanation: List[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime


# Request Schemas
class UserRegisterRequest(BaseModel):
    """Request schema for user registration"""
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    job_type: str = Field(..., min_length=1, max_length=50)
    months_active: int = Field(..., ge=0)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "john@example.com",
                "job_type": "Delivery Driver",
                "months_active": 18
            }
        }


class CalculateScoreRequest(BaseModel):
    """Request schema for score calculation"""
    user_id: str
    avg_income: float = Field(..., ge=0)
    income_variance: float = Field(..., ge=0, le=1)
    upi_txn_count: int = Field(..., ge=0)
    bill_payment_score: int = Field(..., ge=0, le=10)
    withdrawal_ratio: float = Field(..., ge=0, le=1)

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "60d5ec49f1b2c8b1f8e4e1a1",
                "avg_income": 25000.0,
                "income_variance": 0.2,
                "upi_txn_count": 45,
                "bill_payment_score": 8,
                "withdrawal_ratio": 0.5
            }
        }


# Response Schemas
class UserResponse(BaseModel):
    """Response schema for user data"""
    id: str
    name: str
    email: str
    job_type: str
    months_active: int
    created_at: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "id": "60d5ec49f1b2c8b1f8e4e1a1",
                "name": "John Doe",
                "email": "john@example.com",
                "job_type": "Delivery Driver",
                "months_active": 18,
                "created_at": "2024-02-16T10:30:00"
            }
        }


class CreditProfileResponse(BaseModel):
    """Response schema for credit profile"""
    id: str
    user_id: str
    avg_income: float
    income_variance: float
    upi_txn_count: int
    bill_payment_score: int
    withdrawal_ratio: float
    digital_trust_score: int
    risk_category: str
    explanation: List[str]
    created_at: datetime


class ScoreCalculationResponse(BaseModel):
    """Response schema for score calculation"""
    user_id: str
    digital_trust_score: int
    risk_category: str
    explanation: List[str]
    credit_profile_id: str

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "60d5ec49f1b2c8b1f8e4e1a1",
                "digital_trust_score": 75,
                "risk_category": "Low Risk",
                "explanation": [
                    "Stable income pattern detected",
                    "High UPI transaction activity observed",
                    "Regular bill payments recorded"
                ],
                "credit_profile_id": "60d5ec49f1b2c8b1f8e4e1a2"
            }
        }


class UserDetailResponse(BaseModel):
    """Response schema for user details with credit profile"""
    user: UserResponse
    latest_credit_profile: Optional[CreditProfileResponse]

    class Config:
        json_schema_extra = {
            "example": {
                "user": {
                    "id": "60d5ec49f1b2c8b1f8e4e1a1",
                    "name": "John Doe",
                    "email": "john@example.com",
                    "job_type": "Delivery Driver",
                    "months_active": 18,
                    "created_at": "2024-02-16T10:30:00"
                },
                "latest_credit_profile": {
                    "id": "60d5ec49f1b2c8b1f8e4e1a2",
                    "user_id": "60d5ec49f1b2c8b1f8e4e1a1",
                    "digital_trust_score": 75,
                    "risk_category": "Low Risk",
                    "explanation": ["Stable income", "High UPI activity"]
                }
            }
        }

from fastapi import APIRouter, HTTPException, status
from typing import List
from bson import ObjectId
from datetime import datetime

from app.database import get_database
from app.schemas import UserRegisterRequest, UserResponse, UserDetailResponse, CreditProfileResponse
from app.models import UserModel

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserRegisterRequest):
    """
    Register a new user in the system.
    
    Args:
        user_data: User registration information
        
    Returns:
        Created user details
    """
    db = get_database()
    
    # Check if user with email already exists
    existing_user = await db.users.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    # Create user document
    user_dict = user_data.model_dump()
    user_dict["created_at"] = datetime.utcnow()
    
    # Insert into database
    result = await db.users.insert_one(user_dict)
    
    # Fetch and return created user
    created_user = await db.users.find_one({"_id": result.inserted_id})
    
    return UserResponse(
        id=str(created_user["_id"]),
        name=created_user["name"],
        email=created_user["email"],
        job_type=created_user["job_type"],
        months_active=created_user["months_active"],
        created_at=created_user["created_at"]
    )


@router.get("", response_model=List[UserResponse])
async def get_all_users():
    """
    Get all registered users.
    
    Returns:
        List of all users
    """
    db = get_database()
    
    users = []
    cursor = db.users.find({})
    
    async for user in cursor:
        users.append(UserResponse(
            id=str(user["_id"]),
            name=user["name"],
            email=user["email"],
            job_type=user["job_type"],
            months_active=user["months_active"],
            created_at=user["created_at"]
        ))
    
    return users


@router.get("/{user_id}", response_model=UserDetailResponse)
async def get_user_details(user_id: str):
    """
    Get user details along with their latest credit profile.
    
    Args:
        user_id: User ID
        
    Returns:
        User details with latest credit profile
    """
    db = get_database()
    
    # Validate ObjectId
    if not ObjectId.is_valid(user_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )
    
    # Find user
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Get latest credit profile
    credit_profile = await db.credit_profiles.find_one(
        {"user_id": user_id},
        sort=[("created_at", -1)]
    )
    
    user_response = UserResponse(
        id=str(user["_id"]),
        name=user["name"],
        email=user["email"],
        job_type=user["job_type"],
        months_active=user["months_active"],
        created_at=user["created_at"]
    )
    
    credit_profile_response = None
    if credit_profile:
        credit_profile_response = CreditProfileResponse(
            id=str(credit_profile["_id"]),
            user_id=credit_profile["user_id"],
            avg_income=credit_profile["avg_income"],
            income_variance=credit_profile["income_variance"],
            upi_txn_count=credit_profile["upi_txn_count"],
            bill_payment_score=credit_profile["bill_payment_score"],
            withdrawal_ratio=credit_profile["withdrawal_ratio"],
            digital_trust_score=credit_profile["digital_trust_score"],
            risk_category=credit_profile["risk_category"],
            explanation=credit_profile["explanation"],
            created_at=credit_profile["created_at"]
        )
    
    return UserDetailResponse(
        user=user_response,
        latest_credit_profile=credit_profile_response
    )

from fastapi import APIRouter, HTTPException, status
from bson import ObjectId
from datetime import datetime

from app.database import get_database
from app.schemas import CalculateScoreRequest, ScoreCalculationResponse
from app.scoring import calculate_digital_trust_score

router = APIRouter(prefix="/credit", tags=["Credit"])


@router.post("/calculate-score", response_model=ScoreCalculationResponse)
async def calculate_score(score_data: CalculateScoreRequest):
    """
    Calculate Digital Trust Score for a user.
    
    Args:
        score_data: Financial data for score calculation
        
    Returns:
        Calculated score, risk category, and explanations
    """
    db = get_database()
    
    # Validate user exists
    if not ObjectId.is_valid(score_data.user_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )
    
    user = await db.users.find_one({"_id": ObjectId(score_data.user_id)})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Calculate score using scoring logic
    score, risk_category, explanations = calculate_digital_trust_score(
        avg_income=score_data.avg_income,
        income_variance=score_data.income_variance,
        upi_txn_count=score_data.upi_txn_count,
        bill_payment_score=score_data.bill_payment_score,
        withdrawal_ratio=score_data.withdrawal_ratio,
        months_active=user["months_active"]
    )
    
    # Create credit profile document
    credit_profile = {
        "user_id": score_data.user_id,
        "avg_income": score_data.avg_income,
        "income_variance": score_data.income_variance,
        "upi_txn_count": score_data.upi_txn_count,
        "bill_payment_score": score_data.bill_payment_score,
        "withdrawal_ratio": score_data.withdrawal_ratio,
        "digital_trust_score": score,
        "risk_category": risk_category,
        "explanation": explanations,
        "created_at": datetime.utcnow()
    }
    
    # Insert into database
    result = await db.credit_profiles.insert_one(credit_profile)
    
    return ScoreCalculationResponse(
        user_id=score_data.user_id,
        digital_trust_score=score,
        risk_category=risk_category,
        explanation=explanations,
        credit_profile_id=str(result.inserted_id)
    )

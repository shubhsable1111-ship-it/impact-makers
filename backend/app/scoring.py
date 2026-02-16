from typing import List, Tuple


def calculate_digital_trust_score(
    avg_income: float,
    income_variance: float,
    upi_txn_count: int,
    bill_payment_score: int,
    withdrawal_ratio: float,
    months_active: int
) -> Tuple[int, str, List[str]]:
    """
    Calculate Digital Trust Score based on rule-based scoring logic.
    
    Returns:
        Tuple of (score, risk_category, explanations)
    """
    score = 0
    explanations = []

    # Rule 1: Stable income (income_variance < 0.3) → +25
    if income_variance < 0.3:
        score += 25
        explanations.append("Stable income pattern detected with low variance")
    else:
        explanations.append("Income fluctuation detected - consider stabilizing earnings")

    # Rule 2: High UPI activity (upi_txn_count > 30) → +20
    if upi_txn_count > 30:
        score += 20
        explanations.append("High UPI transaction activity observed - strong digital footprint")
    elif upi_txn_count > 15:
        score += 10
        explanations.append("Moderate UPI transaction activity detected")
    else:
        explanations.append("Low digital payment activity - increase UPI usage for better score")

    # Rule 3: Regular bill payments (bill_payment_score > 7) → +20
    if bill_payment_score > 7:
        score += 20
        explanations.append("Regular bill payments recorded - demonstrates financial discipline")
    elif bill_payment_score > 4:
        score += 10
        explanations.append("Occasional bill payments detected")
    else:
        explanations.append("Irregular bill payment history - maintain consistent payments")

    # Rule 4: Work duration ≥ 12 months → +25
    if months_active >= 12:
        score += 25
        explanations.append("Long-term work activity improves trust and stability")
    elif months_active >= 6:
        score += 15
        explanations.append("Moderate work duration demonstrates some commitment")
    else:
        explanations.append("Short work history - longer tenure will improve creditworthiness")

    # Rule 5: High withdrawal ratio (> 0.7) → −10
    if withdrawal_ratio > 0.7:
        score -= 10
        explanations.append("High cash withdrawal behavior increases risk - reduce dependency on cash")
    elif withdrawal_ratio > 0.5:
        explanations.append("Moderate cash withdrawal ratio detected")
    else:
        explanations.append("Low withdrawal ratio indicates good digital transaction habits")

    # Additional insights based on income
    if avg_income > 30000:
        explanations.append("Above-average income level supports creditworthiness")
    elif avg_income > 15000:
        explanations.append("Moderate income level observed")
    else:
        explanations.append("Lower income bracket - focus on building savings and reducing withdrawals")

    # Ensure score stays within 0-100 range
    score = max(0, min(100, score))

    # Determine risk category
    risk_category = classify_risk(score)

    return score, risk_category, explanations


def classify_risk(score: int) -> str:
    """
    Classify risk based on Digital Trust Score.
    
    Args:
        score: Digital Trust Score (0-100)
        
    Returns:
        Risk category string
    """
    if score >= 70:
        return "Low Risk"
    elif score >= 40:
        return "Medium Risk"
    else:
        return "High Risk"


def generate_recommendations(
    score: int,
    risk_category: str,
    income_variance: float,
    upi_txn_count: int,
    bill_payment_score: int,
    withdrawal_ratio: float
) -> List[str]:
    """
    Generate personalized recommendations for improving credit score.
    
    Returns:
        List of recommendation strings
    """
    recommendations = []

    if risk_category == "High Risk":
        recommendations.append("Priority: Focus on building financial stability and digital payment history")

    if income_variance >= 0.3:
        recommendations.append("Try to stabilize your income sources or maintain emergency savings")

    if upi_txn_count <= 30:
        recommendations.append("Increase digital payment usage through UPI for daily transactions")

    if bill_payment_score <= 7:
        recommendations.append("Set up automatic bill payments to improve payment consistency")

    if withdrawal_ratio > 0.7:
        recommendations.append("Reduce cash withdrawals and use digital payments more frequently")

    if score < 70:
        recommendations.append("Continue working in your current role to build a stronger work history")

    return recommendations

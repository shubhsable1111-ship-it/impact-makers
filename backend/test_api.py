"""
Sample API Test Script

This script demonstrates how to use the Credit Risk Assessment API.
Run the FastAPI server first: uvicorn app.main:app --reload
"""

import requests
import json

BASE_URL = "http://localhost:8000"


def print_response(title, response):
    """Pretty print API response"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)
    print(f"Status Code: {response.status_code}")
    print(f"Response:")
    print(json.dumps(response.json(), indent=2))


def main():
    print("🚀 Starting Credit Risk Assessment API Tests...")
    
    # Test 1: Register User
    print("\n📝 Test 1: Register User")
    user_data = {
        "name": "Rajesh Kumar",
        "email": "rajesh.kumar@example.com",
        "job_type": "Delivery Driver",
        "months_active": 18
    }
    
    response = requests.post(f"{BASE_URL}/register", json=user_data)
    print_response("User Registration", response)
    
    if response.status_code == 201:
        user_id = response.json()["id"]
        print(f"\n✅ User registered successfully! User ID: {user_id}")
        
        # Test 2: Calculate Score - High Score Case
        print("\n📊 Test 2: Calculate Score (Expected: Low Risk)")
        score_data = {
            "user_id": user_id,
            "avg_income": 28000.0,
            "income_variance": 0.2,      # Stable income
            "upi_txn_count": 45,          # High UPI activity
            "bill_payment_score": 9,      # Excellent bill payments
            "withdrawal_ratio": 0.4       # Low withdrawals
        }
        
        response = requests.post(f"{BASE_URL}/calculate-score", json=score_data)
        print_response("Score Calculation (Low Risk Expected)", response)
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n🎯 Digital Trust Score: {result['digital_trust_score']}")
            print(f"🏷️  Risk Category: {result['risk_category']}")
            print(f"\n📋 Explanations:")
            for explanation in result['explanation']:
                print(f"  • {explanation}")
        
        # Test 3: Get All Users
        print("\n\n👥 Test 3: Get All Users")
        response = requests.get(f"{BASE_URL}/users")
        print_response("All Users", response)
        
        # Test 4: Get User Details
        print("\n\n🔍 Test 4: Get User Details")
        response = requests.get(f"{BASE_URL}/user/{user_id}")
        print_response("User Details with Credit Profile", response)
        
    # Test 5: Register another user with different profile
    print("\n\n📝 Test 5: Register Second User (Medium Risk Profile)")
    user_data_2 = {
        "name": "Priya Sharma",
        "email": "priya.sharma@example.com",
        "job_type": "Freelance Designer",
        "months_active": 8
    }
    
    response = requests.post(f"{BASE_URL}/register", json=user_data_2)
    print_response("Second User Registration", response)
    
    if response.status_code == 201:
        user_id_2 = response.json()["id"]
        
        # Calculate score for medium risk
        print("\n📊 Test 6: Calculate Score (Expected: Medium Risk)")
        score_data_2 = {
            "user_id": user_id_2,
            "avg_income": 18000.0,
            "income_variance": 0.4,      # Moderate variance
            "upi_txn_count": 25,          # Moderate UPI activity
            "bill_payment_score": 6,      # Average bill payments
            "withdrawal_ratio": 0.6       # Moderate withdrawals
        }
        
        response = requests.post(f"{BASE_URL}/calculate-score", json=score_data_2)
        print_response("Score Calculation (Medium Risk Expected)", response)
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n🎯 Digital Trust Score: {result['digital_trust_score']}")
            print(f"🏷️  Risk Category: {result['risk_category']}")
            print(f"\n📋 Explanations:")
            for explanation in result['explanation']:
                print(f"  • {explanation}")
    
    # Test 7: Register high-risk user
    print("\n\n📝 Test 7: Register Third User (High Risk Profile)")
    user_data_3 = {
        "name": "Amit Patel",
        "email": "amit.patel@example.com",
        "job_type": "Gig Worker",
        "months_active": 3
    }
    
    response = requests.post(f"{BASE_URL}/register", json=user_data_3)
    print_response("Third User Registration", response)
    
    if response.status_code == 201:
        user_id_3 = response.json()["id"]
        
        # Calculate score for high risk
        print("\n📊 Test 8: Calculate Score (Expected: High Risk)")
        score_data_3 = {
            "user_id": user_id_3,
            "avg_income": 12000.0,
            "income_variance": 0.6,      # High variance
            "upi_txn_count": 10,          # Low UPI activity
            "bill_payment_score": 3,      # Poor bill payments
            "withdrawal_ratio": 0.8       # High withdrawals
        }
        
        response = requests.post(f"{BASE_URL}/calculate-score", json=score_data_3)
        print_response("Score Calculation (High Risk Expected)", response)
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n🎯 Digital Trust Score: {result['digital_trust_score']}")
            print(f"🏷️  Risk Category: {result['risk_category']}")
            print(f"\n📋 Explanations:")
            for explanation in result['explanation']:
                print(f"  • {explanation}")
    
    # Test 9: Health Check
    print("\n\n🏥 Test 9: Health Check")
    response = requests.get(f"{BASE_URL}/health")
    print_response("Health Check", response)
    
    print("\n\n" + "="*60)
    print("✅ All tests completed!")
    print("="*60)


if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to API server.")
        print("Please make sure the server is running:")
        print("  uvicorn app.main:app --reload")
    except Exception as e:
        print(f"\n❌ Error: {e}")

"""
Optional ML Module - Placeholder for future machine learning integration.

This module demonstrates how Scikit-learn could be integrated for predictive
credit risk modeling. Currently uses rule-based scoring, but can be extended
with trained models.
"""

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import numpy as np
from typing import Tuple, List
import pickle
import os


class CreditRiskMLModel:
    """
    Placeholder ML model for credit risk prediction.
    
    In production, this would be trained on historical data and used
    to predict credit risk categories.
    """
    
    def __init__(self, model_type: str = "random_forest"):
        """
        Initialize ML model.
        
        Args:
            model_type: Type of model - 'random_forest' or 'logistic_regression'
        """
        self.model_type = model_type
        self.scaler = StandardScaler()
        
        if model_type == "random_forest":
            self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        elif model_type == "logistic_regression":
            self.model = LogisticRegression(random_state=42, max_iter=1000)
        else:
            raise ValueError(f"Unknown model type: {model_type}")
        
        self.is_trained = False
    
    def prepare_features(
        self,
        avg_income: float,
        income_variance: float,
        upi_txn_count: int,
        bill_payment_score: int,
        withdrawal_ratio: float,
        months_active: int
    ) -> np.ndarray:
        """
        Prepare feature vector for ML model.
        
        Returns:
            Feature array
        """
        features = np.array([[
            avg_income,
            income_variance,
            upi_txn_count,
            bill_payment_score,
            withdrawal_ratio,
            months_active
        ]])
        
        return features
    
    def train(self, X: np.ndarray, y: np.ndarray):
        """
        Train the ML model (placeholder - requires real data).
        
        Args:
            X: Feature matrix
            y: Target labels (0: High Risk, 1: Medium Risk, 2: Low Risk)
        """
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train model
        self.model.fit(X_scaled, y)
        self.is_trained = True
        
        print(f"{self.model_type} model trained successfully")
    
    def predict_risk(
        self,
        avg_income: float,
        income_variance: float,
        upi_txn_count: int,
        bill_payment_score: int,
        withdrawal_ratio: float,
        months_active: int
    ) -> Tuple[str, float]:
        """
        Predict credit risk category using ML model.
        
        Returns:
            Tuple of (risk_category, confidence_score)
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        # Prepare features
        features = self.prepare_features(
            avg_income, income_variance, upi_txn_count,
            bill_payment_score, withdrawal_ratio, months_active
        )
        
        # Scale features
        features_scaled = self.scaler.transform(features)
        
        # Predict
        prediction = self.model.predict(features_scaled)[0]
        probabilities = self.model.predict_proba(features_scaled)[0]
        
        # Map prediction to risk category
        risk_map = {0: "High Risk", 1: "Medium Risk", 2: "Low Risk"}
        risk_category = risk_map[prediction]
        confidence = probabilities[prediction]
        
        return risk_category, confidence
    
    def get_feature_importance(self) -> List[Tuple[str, float]]:
        """
        Get feature importance (for Random Forest).
        
        Returns:
            List of (feature_name, importance) tuples
        """
        if not self.is_trained:
            raise ValueError("Model must be trained first")
        
        if self.model_type != "random_forest":
            raise ValueError("Feature importance only available for Random Forest")
        
        feature_names = [
            "avg_income",
            "income_variance",
            "upi_txn_count",
            "bill_payment_score",
            "withdrawal_ratio",
            "months_active"
        ]
        
        importances = self.model.feature_importances_
        
        return sorted(
            zip(feature_names, importances),
            key=lambda x: x[1],
            reverse=True
        )
    
    def save_model(self, filepath: str):
        """Save trained model to disk"""
        if not self.is_trained:
            raise ValueError("Cannot save untrained model")
        
        model_data = {
            "model": self.model,
            "scaler": self.scaler,
            "model_type": self.model_type
        }
        
        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)
        
        print(f"Model saved to {filepath}")
    
    def load_model(self, filepath: str):
        """Load trained model from disk"""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Model file not found: {filepath}")
        
        with open(filepath, 'rb') as f:
            model_data = pickle.load(f)
        
        self.model = model_data["model"]
        self.scaler = model_data["scaler"]
        self.model_type = model_data["model_type"]
        self.is_trained = True
        
        print(f"Model loaded from {filepath}")


# Example usage (for future implementation)
def create_dummy_training_data():
    """
    Create dummy training data for demonstration.
    In production, this would come from historical data.
    """
    np.random.seed(42)
    n_samples = 1000
    
    # Generate synthetic features
    X = np.random.rand(n_samples, 6)
    X[:, 0] *= 50000  # avg_income
    X[:, 1] *= 1      # income_variance
    X[:, 2] *= 100    # upi_txn_count
    X[:, 3] *= 10     # bill_payment_score
    X[:, 4] *= 1      # withdrawal_ratio
    X[:, 5] *= 36     # months_active
    
    # Generate synthetic labels based on simple rules
    y = np.zeros(n_samples, dtype=int)
    for i in range(n_samples):
        score = 0
        if X[i, 1] < 0.3: score += 25
        if X[i, 2] > 30: score += 20
        if X[i, 3] > 7: score += 20
        if X[i, 5] >= 12: score += 25
        if X[i, 4] > 0.7: score -= 10
        
        if score >= 70:
            y[i] = 2  # Low Risk
        elif score >= 40:
            y[i] = 1  # Medium Risk
        else:
            y[i] = 0  # High Risk
    
    return X, y


# Singleton instance (optional)
_ml_model_instance = None


def get_ml_model(model_type: str = "random_forest") -> CreditRiskMLModel:
    """Get or create ML model instance"""
    global _ml_model_instance
    
    if _ml_model_instance is None:
        _ml_model_instance = CreditRiskMLModel(model_type)
    
    return _ml_model_instance

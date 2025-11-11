"""XGBoost model implementation"""
import xgboost as xgb
import pandas as pd
import numpy as np
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, roc_auc_score, mean_squared_error, mean_absolute_error, r2_score
)
from typing import Dict, Any, Optional
import pickle
import json


class XGBoostModel:
    """XGBoost model wrapper for classification and regression"""
    
    def __init__(self, model_type: str = 'classification', **kwargs):
        """
        Initialize XGBoost model
        
        Args:
            model_type: 'classification' or 'regression'
            **kwargs: Parameters to pass to XGBoost model
        """
        self.model_type = model_type
        self.is_trained = False
        
        # Default parameters
        default_params = {
            'max_depth': 5,
            'learning_rate': 0.1,
            'n_estimators': 100,
            'random_state': 42,
            'verbosity': 0,
        }
        
        # Merge with provided parameters
        default_params.update(kwargs)
        
        if model_type == 'classification':
            self.model = xgb.XGBClassifier(**default_params)
        elif model_type == 'regression':
            self.model = xgb.XGBRegressor(**default_params)
        else:
            raise ValueError(f"Unknown model_type: {model_type}")
        
        self.feature_importance = None
        self.metrics = {}
    
    def train(self, X_train: pd.DataFrame, y_train: pd.Series, 
              X_val: Optional[pd.DataFrame] = None, 
              y_val: Optional[pd.Series] = None) -> None:
        """
        Train the XGBoost model
        
        Args:
            X_train: Training features
            y_train: Training target
            X_val: Validation features (optional)
            y_val: Validation target (optional)
        """
        eval_set = None
        if X_val is not None and y_val is not None:
            eval_set = [(X_val, y_val)]
        
        self.model.fit(
            X_train, y_train,
            eval_set=eval_set,
            verbose=False
        )
        
        self.is_trained = True
        self.feature_importance = self._get_feature_importance(X_train)
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """
        Make predictions
        
        Args:
            X: Features to predict on
            
        Returns:
            Predictions
        """
        if not self.is_trained:
            raise ValueError("Model not trained yet. Call train first.")
        return self.model.predict(X)
    
    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """
        Get prediction probabilities (for classification)
        
        Args:
            X: Features to predict on
            
        Returns:
            Probability predictions
        """
        if self.model_type != 'classification':
            raise ValueError("predict_proba only available for classification models")
        if not self.is_trained:
            raise ValueError("Model not trained yet. Call train first.")
        return self.model.predict_proba(X)
    
    def evaluate(self, X_test: pd.DataFrame, y_test: pd.Series) -> Dict[str, float]:
        """
        Evaluate model performance
        
        Args:
            X_test: Test features
            y_test: Test target
            
        Returns:
            Dictionary of metrics
        """
        predictions = self.predict(X_test)
        
        if self.model_type == 'classification':
            self.metrics = {
                'accuracy': accuracy_score(y_test, predictions),
                'precision': precision_score(y_test, predictions, average='weighted', zero_division=0),
                'recall': recall_score(y_test, predictions, average='weighted', zero_division=0),
                'f1': f1_score(y_test, predictions, average='weighted', zero_division=0),
            }
            
            # Try to add ROC-AUC for binary classification
            try:
                if len(np.unique(y_test)) == 2:
                    proba = self.predict_proba(X_test)
                    self.metrics['roc_auc'] = roc_auc_score(y_test, proba[:, 1])
            except:
                pass
        else:  # regression
            y_pred = predictions
            self.metrics = {
                'mse': mean_squared_error(y_test, y_pred),
                'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
                'mae': mean_absolute_error(y_test, y_pred),
                'r2': r2_score(y_test, y_pred),
            }
        
        return self.metrics
    
    def get_feature_importance(self) -> Dict[str, float]:
        """Get feature importance"""
        if self.feature_importance is None:
            raise ValueError("Model not trained yet.")
        return self.feature_importance
    
    def _get_feature_importance(self, X: pd.DataFrame) -> Dict[str, float]:
        """Calculate feature importance"""
        importance = self.model.feature_importances_
        feature_names = X.columns.tolist() if hasattr(X, 'columns') else [f'feature_{i}' for i in range(X.shape[1])]
        # Ensure native Python floats (not numpy types) so tests that check isinstance(..., (int,float)) pass
        importance_list = [float(x) for x in importance]
        return dict(zip(feature_names, importance_list))
    
    def save_model(self, filepath: str) -> None:
        """Save model to file"""
        with open(filepath, 'wb') as f:
            pickle.dump(self.model, f)
    
    def load_model(self, filepath: str) -> None:
        """Load model from file"""
        with open(filepath, 'rb') as f:
            self.model = pickle.load(f)
        self.is_trained = True
    
    def get_params(self) -> Dict[str, Any]:
        """Get model parameters"""
        return self.model.get_params()
    
    def set_params(self, **params) -> None:
        """Set model parameters"""
        self.model.set_params(**params)

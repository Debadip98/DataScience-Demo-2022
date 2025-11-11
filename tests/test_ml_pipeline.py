"""Test module - Unit tests for the ML project"""
import pytest
import pandas as pd
import numpy as np
from src.data_loader import DataLoader
from src.model import XGBoostModel
from src.utils import generate_synthetic_data
import tempfile
import os


class TestDataLoader:
    """Test cases for DataLoader class"""
    
    @pytest.fixture
    def data_loader(self):
        """Create a DataLoader instance"""
        return DataLoader(random_state=42)
    
    @pytest.fixture
    def sample_df(self):
        """Create a sample DataFrame"""
        return generate_synthetic_data(n_samples=100, n_features=5, task='classification')
    
    def test_initialization(self, data_loader):
        """Test DataLoader initialization"""
        assert data_loader.random_state == 42
        assert data_loader.X_train is None
        assert data_loader.X_test is None
    
    def test_handle_missing_values_mean(self, data_loader, sample_df):
        """Test handling missing values with mean method"""
        # Add missing values
        df = sample_df.copy()
        df.iloc[0, 0] = np.nan
        df.iloc[5, 2] = np.nan
        
        # Handle missing values
        result = data_loader.handle_missing_values(df, method='mean')
        
        assert not result.isnull().any().any()
        assert len(result) == len(df)
    
    def test_handle_missing_values_drop(self, data_loader, sample_df):
        """Test handling missing values with drop method"""
        df = sample_df.copy()
        df.iloc[0, 0] = np.nan
        
        result = data_loader.handle_missing_values(df, method='drop')
        
        assert not result.isnull().any().any()
        assert len(result) < len(df)
    
    def test_handle_missing_values_invalid_method(self, data_loader, sample_df):
        """Test handling missing values with invalid method"""
        with pytest.raises(ValueError):
            data_loader.handle_missing_values(sample_df, method='invalid')
    
    def test_prepare_data(self, data_loader, sample_df):
        """Test data preparation"""
        X_train, X_test, y_train, y_test = data_loader.prepare_data(
            sample_df, target_column='target', test_size=0.2
        )
        
        assert X_train.shape[0] == 80
        assert X_test.shape[0] == 20
        assert y_train.shape[0] == 80
        assert y_test.shape[0] == 20
        assert X_train.shape[1] == 10  # 10 features (original features)
    
    def test_prepare_data_invalid_target(self, data_loader, sample_df):
        """Test data preparation with invalid target column"""
        with pytest.raises(ValueError):
            data_loader.prepare_data(sample_df, target_column='invalid_column')
    
    def test_get_train_test_split(self, data_loader, sample_df):
        """Test getting train/test split"""
        data_loader.prepare_data(sample_df, target_column='target')
        X_train, X_test, y_train, y_test = data_loader.get_train_test_split()
        
        assert X_train is not None
        assert X_test is not None
        assert y_train is not None
        assert y_test is not None
    
    def test_get_train_test_split_before_prepare(self, data_loader):
        """Test getting train/test split before prepare_data"""
        with pytest.raises(ValueError):
            data_loader.get_train_test_split()


class TestXGBoostModel:
    """Test cases for XGBoostModel class"""
    
    @pytest.fixture
    def classification_model(self):
        """Create a classification XGBoost model"""
        return XGBoostModel(
            model_type='classification',
            max_depth=3,
            learning_rate=0.1,
            n_estimators=50
        )
    
    @pytest.fixture
    def regression_model(self):
        """Create a regression XGBoost model"""
        return XGBoostModel(
            model_type='regression',
            max_depth=3,
            learning_rate=0.1,
            n_estimators=50
        )
    
    @pytest.fixture
    def classification_data(self):
        """Generate classification data"""
        df = generate_synthetic_data(n_samples=200, n_features=5, task='classification')
        loader = DataLoader(random_state=42)
        return loader.prepare_data(df, target_column='target', test_size=0.2)
    
    @pytest.fixture
    def regression_data(self):
        """Generate regression data"""
        df = generate_synthetic_data(n_samples=200, n_features=5, task='regression')
        loader = DataLoader(random_state=42)
        return loader.prepare_data(df, target_column='target', test_size=0.2)
    
    def test_initialization_classification(self, classification_model):
        """Test model initialization for classification"""
        assert classification_model.model_type == 'classification'
        assert not classification_model.is_trained
    
    def test_initialization_regression(self, regression_model):
        """Test model initialization for regression"""
        assert regression_model.model_type == 'regression'
        assert not regression_model.is_trained
    
    def test_invalid_model_type(self):
        """Test invalid model type"""
        with pytest.raises(ValueError):
            XGBoostModel(model_type='invalid')
    
    def test_train_classification(self, classification_model, classification_data):
        """Test training classification model"""
        X_train, X_test, y_train, y_test = classification_data
        
        classification_model.train(X_train, y_train)
        
        assert classification_model.is_trained
        assert classification_model.feature_importance is not None
    
    def test_train_regression(self, regression_model, regression_data):
        """Test training regression model"""
        X_train, X_test, y_train, y_test = regression_data
        
        regression_model.train(X_train, y_train)
        
        assert regression_model.is_trained
        assert regression_model.feature_importance is not None
    
    def test_train_with_validation(self, classification_model, classification_data):
        """Test training with validation set"""
        X_train, X_test, y_train, y_test = classification_data
        
        classification_model.train(X_train, y_train, X_test, y_test)
        
        assert classification_model.is_trained
    
    def test_predict_classification(self, classification_model, classification_data):
        """Test prediction on classification model"""
        X_train, X_test, y_train, y_test = classification_data
        
        classification_model.train(X_train, y_train)
        predictions = classification_model.predict(X_test)
        
        assert predictions.shape[0] == X_test.shape[0]
        assert len(np.unique(predictions)) <= 2
    
    def test_predict_regression(self, regression_model, regression_data):
        """Test prediction on regression model"""
        X_train, X_test, y_train, y_test = regression_data
        
        regression_model.train(X_train, y_train)
        predictions = regression_model.predict(X_test)
        
        assert predictions.shape[0] == X_test.shape[0]
        assert np.isfinite(predictions).all()
    
    def test_predict_before_train(self, classification_model, classification_data):
        """Test prediction before training"""
        X_train, X_test, y_train, y_test = classification_data
        
        with pytest.raises(ValueError):
            classification_model.predict(X_test)
    
    def test_predict_proba(self, classification_model, classification_data):
        """Test probability predictions"""
        X_train, X_test, y_train, y_test = classification_data
        
        classification_model.train(X_train, y_train)
        proba = classification_model.predict_proba(X_test)
        
        assert proba.shape[0] == X_test.shape[0]
        assert proba.shape[1] == 2
        assert np.allclose(proba.sum(axis=1), 1.0)
    
    def test_predict_proba_regression_error(self, regression_model, regression_data):
        """Test predict_proba raises error for regression"""
        X_train, X_test, y_train, y_test = regression_data
        
        regression_model.train(X_train, y_train)
        
        with pytest.raises(ValueError):
            regression_model.predict_proba(X_test)
    
    def test_evaluate_classification(self, classification_model, classification_data):
        """Test evaluation for classification"""
        X_train, X_test, y_train, y_test = classification_data
        
        classification_model.train(X_train, y_train)
        metrics = classification_model.evaluate(X_test, y_test)
        
        assert 'accuracy' in metrics
        assert 'precision' in metrics
        assert 'recall' in metrics
        assert 'f1' in metrics
        assert all(0 <= v <= 1 for v in metrics.values())
    
    def test_evaluate_regression(self, regression_model, regression_data):
        """Test evaluation for regression"""
        X_train, X_test, y_train, y_test = regression_data
        
        regression_model.train(X_train, y_train)
        metrics = regression_model.evaluate(X_test, y_test)
        
        assert 'mse' in metrics
        assert 'rmse' in metrics
        assert 'mae' in metrics
        assert 'r2' in metrics
    
    def test_get_feature_importance(self, classification_model, classification_data):
        """Test getting feature importance"""
        X_train, X_test, y_train, y_test = classification_data
        
        classification_model.train(X_train, y_train)
        importance = classification_model.get_feature_importance()
        
        assert isinstance(importance, dict)
        assert len(importance) == X_train.shape[1]
        assert all(isinstance(v, (int, float)) for v in importance.values())
    
    def test_get_feature_importance_before_train(self, classification_model):
        """Test getting feature importance before training"""
        with pytest.raises(ValueError):
            classification_model.get_feature_importance()
    
    def test_save_and_load_model(self, classification_model, classification_data):
        """Test saving and loading model"""
        X_train, X_test, y_train, y_test = classification_data
        
        # Train model
        classification_model.train(X_train, y_train)
        original_predictions = classification_model.predict(X_test)
        
        # Save model
        with tempfile.TemporaryDirectory() as tmpdir:
            model_path = os.path.join(tmpdir, 'model.pkl')
            classification_model.save_model(model_path)
            
            # Load model
            new_model = XGBoostModel(model_type='classification')
            new_model.load_model(model_path)
            new_predictions = new_model.predict(X_test)
            
            # Check predictions are identical
            assert np.array_equal(original_predictions, new_predictions)
    
    def test_get_params(self, classification_model):
        """Test getting model parameters"""
        params = classification_model.get_params()
        
        assert isinstance(params, dict)
        assert 'max_depth' in params
        assert 'learning_rate' in params
    
    def test_set_params(self, classification_model):
        """Test setting model parameters"""
        original_depth = classification_model.get_params()['max_depth']
        
        classification_model.set_params(max_depth=10)
        new_depth = classification_model.get_params()['max_depth']
        
        assert new_depth != original_depth
        assert new_depth == 10


class TestIntegration:
    """Integration tests"""
    
    def test_end_to_end_classification(self):
        """Test complete pipeline for classification"""
        # Generate data
        df = generate_synthetic_data(n_samples=300, n_features=8, task='classification')
        
        # Prepare data
        loader = DataLoader(random_state=42)
        X_train, X_test, y_train, y_test = loader.prepare_data(df, target_column='target')
        
        # Train model
        model = XGBoostModel(model_type='classification', n_estimators=100)
        model.train(X_train, y_train)
        
        # Evaluate
        metrics = model.evaluate(X_test, y_test)
        
        assert model.is_trained
        assert metrics['accuracy'] > 0.5  # Should be better than random
        print(f"Classification accuracy: {metrics['accuracy']:.4f}")
    
    def test_end_to_end_regression(self):
        """Test complete pipeline for regression"""
        # Generate data
        df = generate_synthetic_data(n_samples=300, n_features=8, task='regression')
        
        # Prepare data
        loader = DataLoader(random_state=42)
        X_train, X_test, y_train, y_test = loader.prepare_data(df, target_column='target')
        
        # Train model
        model = XGBoostModel(model_type='regression', n_estimators=100)
        model.train(X_train, y_train)
        
        # Evaluate
        metrics = model.evaluate(X_test, y_test)
        
        assert model.is_trained
        assert metrics['r2'] > 0  # Should have positive R2
        print(f"Regression R2: {metrics['r2']:.4f}")


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])

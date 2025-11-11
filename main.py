"""
Main script demonstrating the complete ML pipeline
"""
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.data_loader import DataLoader
from src.model import XGBoostModel
from src.utils import generate_synthetic_data, print_metrics, plot_feature_importance


def main():
    """Run the complete ML pipeline"""
    print("\n" + "="*70)
    print("XGBoost Machine Learning Pipeline - End-to-End Example")
    print("="*70 + "\n")
    
    # Step 1: Generate synthetic data
    print("Step 1: Generating synthetic data...")
    df = generate_synthetic_data(n_samples=500, n_features=15, task='classification', random_state=42)
    print(f"Generated dataset shape: {df.shape}")
    print(f"Data types:\n{df.dtypes}\n")
    
    # Step 2: Data preparation
    print("Step 2: Preparing data...")
    loader = DataLoader(random_state=42)
    
    # Handle any missing values (there are none in synthetic data, but showing the method)
    df_clean = loader.handle_missing_values(df, method='mean')
    print(f"Data after handling missing values: {df_clean.shape}")
    
    # Split data
    X_train, X_test, y_train, y_test = loader.prepare_data(
        df_clean, 
        target_column='target',
        test_size=0.2
    )
    print(f"Training set shape: {X_train.shape}")
    print(f"Test set shape: {X_test.shape}")
    print(f"Training target distribution:\n{y_train.value_counts()}\n")
    
    # Step 3: Model creation and training
    print("Step 3: Creating and training XGBoost model...")
    model = XGBoostModel(
        model_type='classification',
        max_depth=6,
        learning_rate=0.1,
        n_estimators=150,
        random_state=42
    )
    
    print("Training model...")
    model.train(X_train, y_train, X_val=X_test, y_val=y_test)
    print("Model trained successfully!\n")
    
    # Step 4: Evaluation
    print("Step 4: Evaluating model...")
    metrics = model.evaluate(X_test, y_test)
    print_metrics(metrics, metric_type='classification')
    
    # Step 5: Feature importance
    print("Step 5: Analyzing feature importance...")
    feature_importance = model.get_feature_importance()
    
    print("\nTop 10 most important features:")
    sorted_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)
    for i, (feature, importance) in enumerate(sorted_features[:10], 1):
        print(f"{i:2d}. {feature:<15} {importance:.6f}")
    
    # Step 6: Making predictions
    print("\nStep 6: Making predictions on new data...")
    sample_predictions = model.predict(X_test[:5])
    sample_proba = model.predict_proba(X_test[:5])
    
    print("\nSample predictions (first 5 test samples):")
    print(f"Predictions: {sample_predictions}")
    print(f"\nProbabilities:")
    for i, proba in enumerate(sample_proba):
        print(f"Sample {i}: Class 0: {proba[0]:.4f}, Class 1: {proba[1]:.4f}")
    
    # Step 7: Saving model
    print("\n\nStep 7: Saving model...")
    model_path = 'models/xgboost_model.pkl'
    os.makedirs('models', exist_ok=True)
    model.save_model(model_path)
    print(f"Model saved to: {model_path}\n")
    
    print("="*70)
    print("Pipeline completed successfully!")
    print("="*70 + "\n")


if __name__ == '__main__':
    main()

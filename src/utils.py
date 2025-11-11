"""Utility functions for the ML project"""
import pandas as pd
import numpy as np
from typing import Dict, List
import matplotlib.pyplot as plt
import seaborn as sns


def generate_synthetic_data(n_samples: int = 1000, n_features: int = 10, 
                           task: str = 'classification', random_state: int = 42) -> pd.DataFrame:
    """
    Generate synthetic dataset for testing
    
    Args:
        n_samples: Number of samples
        n_features: Number of features
        task: 'classification' or 'regression'
        random_state: Random state for reproducibility
        
    Returns:
        DataFrame with synthetic data
    """
    np.random.seed(random_state)
    
    X = np.random.randn(n_samples, n_features)
    
    if task == 'classification':
        # Create a simple classification problem
        coefficients = np.random.randn(n_features)
        y = (X @ coefficients > 0).astype(int)
    else:  # regression
        coefficients = np.random.randn(n_features)
        y = X @ coefficients + np.random.randn(n_samples) * 0.1
    
    # Create DataFrame
    feature_names = [f'feature_{i}' for i in range(n_features)]
    df = pd.DataFrame(X, columns=feature_names)
    df['target'] = y
    
    return df


def plot_feature_importance(feature_importance: Dict[str, float], top_n: int = 10, 
                           figsize: tuple = (10, 6)) -> None:
    """
    Plot feature importance
    
    Args:
        feature_importance: Dictionary of feature importance
        top_n: Number of top features to display
        figsize: Figure size
    """
    # Sort by importance
    sorted_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)
    top_features = sorted_features[:top_n]
    
    features, importances = zip(*top_features)
    
    plt.figure(figsize=figsize)
    sns.barplot(x=list(importances), y=list(features), palette='viridis')
    plt.xlabel('Importance')
    plt.ylabel('Feature')
    plt.title(f'Top {top_n} Feature Importance')
    plt.tight_layout()
    plt.savefig('feature_importance.png', dpi=300, bbox_inches='tight')
    print("Feature importance plot saved as 'feature_importance.png'")


def plot_confusion_matrix(y_true: np.ndarray, y_pred: np.ndarray, figsize: tuple = (8, 6)) -> None:
    """
    Plot confusion matrix
    
    Args:
        y_true: True labels
        y_pred: Predicted labels
        figsize: Figure size
    """
    from sklearn.metrics import confusion_matrix
    
    cm = confusion_matrix(y_true, y_pred)
    
    plt.figure(figsize=figsize)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=True)
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.title('Confusion Matrix')
    plt.tight_layout()
    plt.savefig('confusion_matrix.png', dpi=300, bbox_inches='tight')
    print("Confusion matrix plot saved as 'confusion_matrix.png'")


def print_metrics(metrics: Dict[str, float], metric_type: str = 'classification') -> None:
    """
    Print evaluation metrics in a formatted way
    
    Args:
        metrics: Dictionary of metrics
        metric_type: 'classification' or 'regression'
    """
    print("\n" + "="*50)
    print(f"{metric_type.upper()} METRICS")
    print("="*50)
    for metric_name, value in metrics.items():
        print(f"{metric_name.upper():.<30} {value:.4f}")
    print("="*50 + "\n")

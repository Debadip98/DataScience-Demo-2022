# XGBoost End-to-End ML Project

A complete machine learning project demonstrating XGBoost for both classification and regression tasks, with comprehensive test cases and utilities.

## 📁 Project Structure

```
├── src/
│   ├── __init__.py
│   ├── data_loader.py       # Data loading and preprocessing
│   ├── model.py             # XGBoost model wrapper
│   └── utils.py             # Utility functions
├── tests/
│   └── test_ml_pipeline.py  # Comprehensive test suite
├── data/                    # Data storage
├── models/                  # Trained models
├── notebooks/               # Jupyter notebooks
├── main.py                  # Main pipeline script
├── requirements.txt         # Project dependencies
└── README.md               # This file
```

## 🚀 Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

### Running the Pipeline

```bash
# Run the complete ML pipeline
python main.py
```

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_ml_pipeline.py -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

## 📚 Components

### 1. **DataLoader** (`src/data_loader.py`)

Handles data loading, preprocessing, and train/test splitting.

```python
from src.data_loader import DataLoader

loader = DataLoader(random_state=42)

# Load data
df = pd.read_csv('data.csv')

# Handle missing values
df = loader.handle_missing_values(df, method='mean')

# Prepare data for modeling
X_train, X_test, y_train, y_test = loader.prepare_data(
    df, 
    target_column='target',
    test_size=0.2
)
```

**Key Methods:**
- `load_data()` - Load CSV files
- `handle_missing_values()` - Handle missing data (mean, median, drop)
- `prepare_data()` - Split and scale data
- `get_train_test_split()` - Retrieve prepared data

### 2. **XGBoostModel** (`src/model.py`)

Wrapper for XGBoost models supporting both classification and regression.

```python
from src.model import XGBoostModel

# Create model
model = XGBoostModel(
    model_type='classification',
    max_depth=5,
    learning_rate=0.1,
    n_estimators=100
)

# Train
model.train(X_train, y_train, X_val=X_test, y_val=y_test)

# Predict
predictions = model.predict(X_test)
probabilities = model.predict_proba(X_test)

# Evaluate
metrics = model.evaluate(X_test, y_test)

# Feature importance
importance = model.get_feature_importance()

# Save/Load
model.save_model('model.pkl')
model.load_model('model.pkl')
```

**Key Methods:**
- `train()` - Train the model
- `predict()` - Make predictions
- `predict_proba()` - Get prediction probabilities (classification)
- `evaluate()` - Evaluate model performance
- `get_feature_importance()` - Get feature importance
- `save_model()` / `load_model()` - Model persistence

**Supported Metrics:**

*Classification:*
- Accuracy
- Precision (weighted)
- Recall (weighted)
- F1-Score (weighted)
- ROC-AUC (for binary classification)

*Regression:*
- Mean Squared Error (MSE)
- Root Mean Squared Error (RMSE)
- Mean Absolute Error (MAE)
- R² Score

### 3. **Utilities** (`src/utils.py`)

Helper functions for data generation, visualization, and reporting.

```python
from src.utils import generate_synthetic_data, print_metrics, plot_feature_importance

# Generate synthetic data
df = generate_synthetic_data(n_samples=1000, n_features=10, task='classification')

# Print metrics
print_metrics(metrics, metric_type='classification')

# Plot feature importance
plot_feature_importance(importance, top_n=10)
```

## 🧪 Test Suite

Comprehensive test coverage with 40+ test cases:

### Test Categories

1. **DataLoader Tests** (10 tests)
   - Initialization
   - Missing value handling (mean, median, drop)
   - Data preparation and splitting
   - Error handling

2. **XGBoostModel Tests** (20+ tests)
   - Model initialization
   - Training (with/without validation)
   - Predictions (classification & regression)
   - Probability predictions
   - Model evaluation
   - Feature importance
   - Model persistence (save/load)
   - Parameter management

3. **Integration Tests** (2 tests)
   - End-to-end classification pipeline
   - End-to-end regression pipeline

### Running Tests

```bash
# Run all tests with verbose output
pytest tests/test_ml_pipeline.py -v

# Run specific test class
pytest tests/test_ml_pipeline.py::TestXGBoostModel -v

# Run specific test
pytest tests/test_ml_pipeline.py::TestDataLoader::test_prepare_data -v

# Generate coverage report
pytest tests/ --cov=src --cov-report=html
```

## 📊 Usage Examples

### Classification Example

```python
from src.data_loader import DataLoader
from src.model import XGBoostModel
from src.utils import generate_synthetic_data

# 1. Generate data
df = generate_synthetic_data(n_samples=500, n_features=10, task='classification')

# 2. Prepare data
loader = DataLoader()
X_train, X_test, y_train, y_test = loader.prepare_data(df, target_column='target')

# 3. Train model
model = XGBoostModel(model_type='classification', n_estimators=100)
model.train(X_train, y_train)

# 4. Evaluate
metrics = model.evaluate(X_test, y_test)
print(f"Accuracy: {metrics['accuracy']:.4f}")
print(f"F1-Score: {metrics['f1']:.4f}")
```

### Regression Example

```python
from src.data_loader import DataLoader
from src.model import XGBoostModel
from src.utils import generate_synthetic_data

# 1. Generate data
df = generate_synthetic_data(n_samples=500, n_features=10, task='regression')

# 2. Prepare data
loader = DataLoader()
X_train, X_test, y_train, y_test = loader.prepare_data(df, target_column='target')

# 3. Train model
model = XGBoostModel(model_type='regression', n_estimators=100)
model.train(X_train, y_train)

# 4. Evaluate
metrics = model.evaluate(X_test, y_test)
print(f"RMSE: {metrics['rmse']:.4f}")
print(f"R² Score: {metrics['r2']:.4f}")
```

## 🔧 Model Parameters

### XGBoostModel Configuration

```python
model = XGBoostModel(
    model_type='classification',  # 'classification' or 'regression'
    max_depth=5,                  # Maximum tree depth
    learning_rate=0.1,            # Learning rate (eta)
    n_estimators=100,             # Number of boosting rounds
    random_state=42,              # Random seed for reproducibility
    # Additional XGBoost parameters can be passed
)
```

## 📈 Performance Tips

1. **Feature Engineering**: Use domain knowledge to create meaningful features
2. **Hyperparameter Tuning**: Grid search or random search for optimal parameters
3. **Cross-Validation**: Use k-fold cross-validation for robust evaluation
4. **Data Scaling**: Always scale features (already done in DataLoader)
5. **Class Imbalance**: Handle imbalanced datasets with appropriate metrics

## 🐛 Troubleshooting

### Common Issues

**Issue**: ImportError when running main.py
- **Solution**: Make sure you're in the project root directory and src/ is a Python package

**Issue**: Tests fail with "No such file or directory"
- **Solution**: Run tests from the project root: `pytest tests/`

**Issue**: Memory error with large datasets
- **Solution**: Reduce `n_estimators` or use `tree_method='gpu_hist'` if GPU is available

## 📦 Dependencies

- **xgboost**: Gradient boosting framework
- **scikit-learn**: Machine learning utilities
- **pandas**: Data manipulation
- **numpy**: Numerical computations
- **matplotlib**: Visualization
- **seaborn**: Advanced visualization
- **pytest**: Testing framework

See `requirements.txt` for versions.

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## 📧 Contact

For questions or suggestions, please open an issue on GitHub.

---

**Happy ML Modeling! 🚀**

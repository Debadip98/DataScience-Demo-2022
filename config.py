"""
Configuration file for the ML project
"""

# Model configuration
MODEL_CONFIG = {
    'classification': {
        'max_depth': 5,
        'learning_rate': 0.1,
        'n_estimators': 100,
        'objective': 'binary:logistic',
    },
    'regression': {
        'max_depth': 5,
        'learning_rate': 0.1,
        'n_estimators': 100,
        'objective': 'reg:squarederror',
    }
}

# Data configuration
DATA_CONFIG = {
    'test_size': 0.2,
    'random_state': 42,
    'scaling': True,
}

# Paths
PATHS = {
    'data_dir': 'data/',
    'model_dir': 'models/',
    'results_dir': 'results/',
}

# XGBoost ML Dashboard - Complete Setup Guide

## 📋 Quick Start

### Option 1: Local Development (Recommended for Development)

```bash
# Install dependencies
make install

# Run development environment
make dev
```

Visit `http://localhost:5000` for the dashboard.

### Option 2: Docker (Recommended for Production)

```bash
# Build and run with Docker
make docker-run

# Or use docker-compose
docker-compose up -d
```

Visit `http://localhost` to access the application.

---

## 🚀 Available Commands

### Development Commands

```bash
make help          # Display all available commands
make install       # Install all dependencies
make dev-setup     # Setup complete development environment
make dev           # Run frontend + backend in development mode
```

### Code Quality

```bash
make lint          # Run linting checks (flake8)
make format        # Format code (black, isort)
make security      # Run security scans (bandit, safety)
```

### Testing

```bash
make test          # Run all tests
make test-cov      # Run tests with coverage report
make check         # Run all checks: lint, security, test
```

### Running the Application

```bash
make run           # Run Flask development server
make run-prod      # Run Flask with gunicorn (production)
make dev           # Run both backend and frontend
```

### Frontend Commands

```bash
make frontend-install   # Install npm dependencies
make frontend-dev       # Run frontend dev server
make frontend-build     # Build frontend assets
```

### Docker Commands

```bash
make docker-build   # Build Docker image
make docker-run     # Build and run Docker container
make docker-stop    # Stop Docker container
make docker-clean   # Remove Docker containers and images
```

### Cleanup

```bash
make clean          # Clean up generated files
make deep-clean     # Complete cleanup (including venv, node_modules)
```

### Utilities

```bash
make status         # Show project status
make requirements-freeze  # Freeze Python dependencies
```

---

## 🏗️ Project Structure

```
DataScience-Demo-2022/
├── .github/workflows/
│   └── ci.yml                 # GitHub Actions CI/CD pipeline
├── app.py                     # Flask application
├── config.py                  # Configuration settings
├── Makefile                   # Build automation
├── Dockerfile                 # Container configuration
├── docker-compose.yml         # Multi-container orchestration
├── nginx.conf                 # Nginx reverse proxy config
├── requirements.txt           # Python dependencies
│
├── src/                       # ML model source code
│   ├── __init__.py
│   ├── data_loader.py         # Data loading & preprocessing
│   ├── model.py               # XGBoost model wrapper
│   └── utils.py               # Utility functions
│
├── tests/                     # Unit tests
│   └── test_ml_pipeline.py
│
├── frontend/                  # Web UI
│   ├── package.json           # npm dependencies
│   ├── templates/
│   │   └── index.html         # Main HTML page
│   └── static/
│       ├── css/
│       │   └── style.css      # Styling (1000+ lines, fully responsive)
│       └── js/
│           ├── api.js         # API client functions
│           ├── ui.js          # UI utilities
│           ├── charts.js      # Chart.js integration
│           └── main.js        # Main application logic
│
├── data/                      # Data directory
├── models/                    # Trained models
├── notebooks/                 # Jupyter notebooks
│   └── XGBoost_Pipeline.ipynb
│
├── README.md                  # Main README
├── README_PROJECT.md          # ML project documentation
└── SETUP.md                   # This file
```

---

## 💻 Technologies Used

### Backend
- **Python 3.12**: Core language
- **Flask**: Web framework
- **XGBoost**: Machine learning model
- **scikit-learn**: ML utilities
- **pandas/numpy**: Data processing
- **Gunicorn**: Production WSGI server

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling (1000+ lines, responsive design)
- **JavaScript (ES6+)**: Interactive features
- **Chart.js**: Data visualization
- **Bootstrap Icons**: Icon library

### DevOps & CI/CD
- **GitHub Actions**: Automated testing & deployment
- **Docker**: Containerization
- **docker-compose**: Multi-container orchestration
- **Nginx**: Reverse proxy

### Development Tools
- **pytest**: Unit testing
- **flake8**: Linting
- **black**: Code formatting
- **bandit**: Security scanning
- **coverage**: Test coverage reporting

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DEBUG=True

# API Configuration
API_WORKERS=4
API_TIMEOUT=30

# Database (if applicable)
DATABASE_URL=sqlite:///app.db

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log

# Model Configuration
MODEL_PATH=models/xgboost_model.pkl
DATA_PATH=data/
```

### Flask Configuration (config.py)

```python
import os

class Config:
    """Base configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key')
    JSON_SORT_KEYS = False

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
```

---

## 🐳 Docker Setup

### Build Docker Image

```bash
make docker-build
```

### Run with Docker Compose

```bash
docker-compose up -d
```

### Access Services

- Backend API: `http://localhost:5000/api`
- Frontend UI: `http://localhost:3000` or `http://localhost`
- Nginx Proxy: `http://localhost:80`

### Docker Compose Services

1. **backend**: Flask API on port 5000
2. **frontend**: Node.js frontend on port 3000
3. **nginx**: Reverse proxy on port 80

### Useful Docker Commands

```bash
# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Execute command in container
docker-compose exec backend python -c "import src.model"

# Stop and remove
docker-compose down

# Remove volumes too
docker-compose down -v
```

---

## 🧪 Testing

### Run All Tests

```bash
make test
```

### Run Tests with Coverage

```bash
make test-cov
```

This generates an HTML coverage report in `htmlcov/index.html`.

### Run Specific Tests

```bash
pytest tests/test_ml_pipeline.py::TestDataLoader -v
pytest tests/test_ml_pipeline.py::TestXGBoostModel::test_train_classification -v
```

### Test Structure

```
tests/
├── test_ml_pipeline.py
│   ├── TestDataLoader (10 tests)
│   ├── TestXGBoostModel (20+ tests)
│   └── TestIntegration (2 tests)
```

---

## 📊 API Endpoints

### Health Check
```
GET /api/health
Response: { status: "healthy", model_loaded: true, version: "1.0.0" }
```

### Model Information
```
GET /api/model/info
Response: { type: "classification", is_trained: true, parameters: {...}, feature_importance: {...} }
```

### Single Prediction
```
POST /api/predict
Body: { "features": [0.5, -0.2, 1.3, ...] }
Response: { prediction: 1, probabilities: { class_0: 0.25, class_1: 0.75 }, confidence: 0.75 }
```

### Batch Predictions
```
POST /api/predict/batch
Body: { "records": [[...], [...], ...] }
Response: { predictions: [{...}, {...}, ...] }
```

### Feature Importance
```
GET /api/feature-importance
Response: { importance: {...}, top_10: {...} }
```

### Model Metrics
```
GET /api/metrics
Response: { accuracy: 0.87, precision: 0.89, recall: 0.85, f1: 0.87 }
```

### Generate Sample
```
GET /api/generate-sample
Response: { features: [0.123, -0.456, ...] }
```

---

## 🎨 Frontend Features

### Pages
1. **Home**: Hero section with quick stats
2. **Predict**: Input features and get predictions
3. **Analytics**: Model visualization and metrics
4. **About**: Project information

### Interactive Features
- Real-time predictions
- Batch processing
- Feature importance visualization
- Model metrics dashboard
- Responsive design (mobile, tablet, desktop)
- Dark-mode compatible CSS

### Keyboard Shortcuts
- `Alt + H`: Go to Home
- `Alt + P`: Go to Prediction
- `Alt + A`: Go to Analytics

---

## 🔐 Security Features

### Application Level
- Input validation on all API endpoints
- Rate limiting on API calls
- CORS configuration for cross-origin requests
- Error handling without sensitive information leakage

### Network Level (Nginx)
- Security headers (X-Frame-Options, X-Content-Type-Options, etc.)
- CORS headers
- Gzip compression
- Rate limiting per IP

### DevOps Level
- Non-root user in Docker containers
- Health checks
- Secure logging
- Bandit security scanning in CI/CD

---

## 📈 CI/CD Pipeline

### GitHub Actions Workflow

The `.github/workflows/ci.yml` includes:

1. **Python Backend Tests** (Ubuntu Latest)
   - Dependency installation
   - Linting with flake8
   - Code formatting checks
   - Unit tests with pytest
   - Coverage reporting

2. **Frontend Tests** (Ubuntu Latest)
   - Node.js setup
   - Dependency installation
   - Code linting
   - Build verification

3. **Security Scanning**
   - Bandit for Python security
   - Safety for dependency vulnerabilities

4. **Docker Build**
   - Multi-stage Docker build
   - Image caching optimization

5. **Deployment Check**
   - Verification all tests passed
   - Readiness confirmation

### Trigger Events
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop`

---

## 🚨 Troubleshooting

### Issue: Port already in use
```bash
# Find process using port 5000
lsof -i :5000
kill -9 <PID>

# Or use different port
FLASK_PORT=5001 make run
```

### Issue: Module not found errors
```bash
# Ensure virtual environment is activated
make install
# or manually
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### Issue: API connection errors in frontend
```bash
# Check if backend is running
curl http://localhost:5000/api/health

# Check CORS headers
curl -I http://localhost:5000/api/health
```

### Issue: Docker image build failures
```bash
# Clean build
make docker-clean
make docker-build

# Or with verbose output
docker-compose build --no-cache
```

---

## 📚 Additional Resources

### Documentation
- [XGBoost Documentation](https://xgboost.readthedocs.io/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [scikit-learn Documentation](https://scikit-learn.org/)
- [Docker Documentation](https://docs.docker.com/)

### Files to Read
- `README.md` - Project overview
- `README_PROJECT.md` - ML project details
- `Makefile` - Available commands
- `.github/workflows/ci.yml` - CI/CD configuration

---

## 📝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/name`
3. Make your changes
4. Run tests: `make test`
5. Run linting: `make lint`
6. Commit: `git commit -am 'Add feature'`
7. Push: `git push origin feature/name`
8. Open a pull request

---

## 📄 License

MIT License - See LICENSE file for details

---

## 🤝 Support

For issues, questions, or suggestions:
1. Check existing documentation
2. Review troubleshooting section
3. Open an issue on GitHub
4. Contact the maintainer

---

**Happy Machine Learning! 🚀**

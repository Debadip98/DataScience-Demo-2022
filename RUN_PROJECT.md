# How to Run the Project

This guide covers all ways to run the DataScience XGBoost ML project locally, in development, and in production.

---

## Table of Contents

1. [Quick Start (Local)](#quick-start-local)
2. [Detailed Local Setup](#detailed-local-setup)
3. [Run Individual Components](#run-individual-components)
4. [Docker & Production](#docker--production)
5. [Using the Makefile](#using-the-makefile)

---

## Quick Start (Local)

### Prerequisites
- Python 3.12+
- Node.js 18+ (for frontend)
- pip or conda

### One-Command Setup & Run

```bash
# Clone the repo (if not already done)
git clone https://github.com/Debadip98/DataScience-Demo-2022.git
cd DataScience-Demo-2022

# Create virtual environment and install dependencies
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install -r dev-requirements.txt

# Run all tests
pytest tests/ -v

# Run the Flask backend (development server on http://localhost:5000)
python app.py

# In another terminal, run the frontend (on http://localhost:8000)
cd frontend
npm install
npm start
```

Then open your browser to:
- **Backend API**: http://localhost:5000
- **Frontend Dashboard**: http://localhost:8000

---

## Detailed Local Setup

### Step 1: Set Up Python Environment

```bash
# Create a virtual environment
python -m venv .venv

# Activate it
# On macOS/Linux:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip
```

### Step 2: Install Dependencies

```bash
# Install runtime dependencies
pip install -r requirements.txt

# Install development tools (testing, linting, formatting)
pip install -r dev-requirements.txt
```

### Step 3: Verify Installation

```bash
# Test Python imports
python -c "import xgboost, pandas, numpy, flask; print('✓ All packages installed')"

# Run the test suite
pytest tests/ -v --cov=src --cov=app --cov-report=html
```

---

## Run Individual Components

### 1. Run the ML Pipeline (Training & Inference)

```bash
# Train an XGBoost model and save predictions
python main.py
```

**Output:**
- Trained model saved to `models/xgboost_model.pkl`
- Evaluation metrics printed to console
- Sample predictions generated

### 2. Run the Flask Backend API Server

```bash
# Development mode (auto-reload)
python app.py

# Or using Flask CLI
FLASK_APP=app.py FLASK_ENV=development flask run

# Or using gunicorn (production-like)
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

**Available Endpoints:**
- `GET  /api/health` — Check backend status
- `GET  /api/model/info` — Model metadata
- `POST /api/predict` — Single prediction (JSON body with features)
- `POST /api/predict/batch` — Batch predictions
- `GET  /api/feature-importance` — Feature importance scores
- `GET  /api/metrics` — Model evaluation metrics
- `POST /api/generate-sample` — Generate synthetic sample

**Example request:**
```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"feature_0": 0.5, "feature_1": -0.2, "feature_2": 1.1, "feature_3": 0.8, "feature_4": -0.3}'
```

### 3. Run the Frontend (React/Static)

```bash
cd frontend

# Install dependencies (one-time)
npm install

# Start development server (http://localhost:8000)
npm start

# Or build for production
npm run build
```

### 4. Run Tests

```bash
# Run all unit and integration tests
pytest tests/ -v

# Run with coverage report
pytest tests/ -v --cov=src --cov=app --cov-report=html

# Run specific test file
pytest tests/test_ml_pipeline.py -v

# Run specific test
pytest tests/test_ml_pipeline.py::TestDataLoader::test_prepare_data -v
```

### 5. Code Quality & Linting

```bash
# Format code with black
black src/ tests/ app/

# Sort imports with isort
isort src/ tests/ app/

# Lint with flake8
flake8 src/ tests/ app/ --max-line-length=127

# Check for security issues
bandit -r src/ app/

# Check dependencies for vulnerabilities
safety check
```

---

## Docker & Production

### Build & Run with Docker Compose

The easiest way to run the entire stack locally (backend + frontend + nginx):

```bash
# Build images
docker-compose build

# Run all services
docker-compose up

# Run in background
docker-compose up -d
```

**Services started:**
- **Backend API**: http://localhost:5000 (via gunicorn)
- **Frontend**: http://localhost (via nginx + static server)
- **Nginx reverse proxy**: Routes `/api` to backend, `/` to frontend

**View logs:**
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
```

**Stop services:**
```bash
docker-compose down
```

### Build Docker Image Only

```bash
# Build
docker build -t xgboost-ml-app:latest .

# Run
docker run -p 5000:5000 xgboost-ml-app:latest

# Run with mounted code (development)
docker run -v $(pwd):/app -p 5000:5000 xgboost-ml-app:latest
```

---

## Using the Makefile

The project includes a `Makefile` with common tasks:

```bash
# View all available targets
make help

# Install dependencies
make install

# Run code formatters
make format

# Run linters
make lint

# Run tests
make test

# Run backend server
make run

# Run in development mode (auto-reload)
make dev

# Build Docker image
make docker-build

# Run Docker Compose
make docker-run

# Clean build artifacts
make clean
```

### Example Workflow

```bash
# Install dependencies
make install

# Format and lint code
make format
make lint

# Run tests
make test

# Start development server
make dev
```

---

## Environment Configuration

### Create a `.env` File (Optional)

```bash
# Copy example
cp .env.example .env

# Edit for your environment
# Common variables:
FLASK_ENV=development      # or 'production'
FLASK_DEBUG=True           # Enable debug mode
SECRET_KEY=your-secret-key # Flask secret
```

---

## Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'src'`
**Solution:** Ensure PYTHONPATH is set:
```bash
PYTHONPATH=$(pwd) python main.py
```

Or add to `.env`:
```
export PYTHONPATH=$(pwd)
```

### Issue: Port 5000 already in use
**Solution:** Use a different port:
```bash
python -c "from app import app; app.run(port=5001)"
```

Or with Flask CLI:
```bash
FLASK_ENV=development FLASK_RUN_PORT=5001 flask run
```

### Issue: Tests fail with import errors
**Solution:** Activate the virtual environment and set PYTHONPATH:
```bash
source .venv/bin/activate
PYTHONPATH=$(pwd) pytest tests/ -v
```

### Issue: Frontend not connecting to backend
**Solution:** Ensure the backend is running on http://localhost:5000 and check CORS is enabled (it is by default in `app.py`).

---

## Performance Tips

### For Development
- Use `python app.py` (Flask development server) for quick iterations
- Enable auto-reload: `FLASK_DEBUG=True python app.py`

### For Testing
- Run tests in parallel: `pytest -n auto tests/`
- Run with coverage: `pytest --cov=src --cov=app tests/`

### For Production
- Use gunicorn with multiple workers: `gunicorn -w 4 -b 0.0.0.0:5000 app:app`
- Use Docker Compose for full stack isolation
- Set `FLASK_ENV=production`

---

## Next Steps

- **API Documentation**: See `app.py` docstrings for endpoint details
- **Model Training**: Run `python main.py` to retrain the XGBoost model
- **CI/CD**: GitHub Actions runs tests on every push; see `.github/workflows/ci.yml`
- **Deployment**: Use Docker Compose or deploy to cloud (AWS, GCP, Azure, Heroku)

---

## Contact & Support

For issues or questions, check the main `README.md` or create a GitHub issue.

Happy hacking! 🚀

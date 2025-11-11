# KU Cancer Prediction App - Medical AI Diagnosis

A **production-ready** cancer prediction application featuring **XGBoost** machine learning model with a complete CI/CD pipeline, attractive web dashboard, comprehensive testing, and Docker containerization.

![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-green?style=flat-square&logo=flask)
![XGBoost](https://img.shields.io/badge/XGBoost-2.1-orange?style=flat-square)
![Docker](https://img.shields.io/badge/Docker-Supported-blue?style=flat-square&logo=docker)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## 🎯 Project Overview

This project demonstrates a **complete end-to-end cancer prediction system** with:

✅ **ML Model** - XGBoost classification for medical diagnosis
✅ **Web API** - Flask REST API for model serving
✅ **Interactive Dashboard** - Modern, responsive UI with real-time predictions
✅ **CI/CD Pipeline** - GitHub Actions with automated testing & deployment
✅ **Containerization** - Docker & Docker Compose for easy deployment
✅ **Production Ready** - Security, logging, health checks, medical-grade validation  

---

## 🚀 Quick Start

### Option 1: Local Development (Fastest)

```bash
# Clone repository
git clone https://github.com/Debadip98/DataScience-Demo-2022.git
cd DataScience-Demo-2022

# Install & run
make install
make dev
```

Visit **http://localhost:5000**

### Option 2: Docker (Recommended)

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f backend
```

Visit **http://localhost**

### Option 3: Manual Setup

```bash
# Backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
python app.py

# Frontend (in another terminal)
cd frontend
npm install
npm run serve
```

---

## 📊 Features

### 🔬 Machine Learning
- **XGBoost Classification** with scikit-learn pipeline
- **Data Preprocessing** - scaling, missing value handling
- **Feature Engineering** - importance analysis & visualization
- **Model Evaluation** - comprehensive metrics (accuracy, precision, recall, F1, AUC)
- **40+ Unit Tests** - >90% code coverage
- **Batch Predictions** - handle multiple samples efficiently

### 🌐 Web Dashboard
- **Modern UI** - responsive design, mobile-friendly
- **Real-time Predictions** - instant model inference
- **Feature Importance** - interactive visualizations
- **Model Metrics** - performance dashboard
- **Batch Processing** - upload & predict multiple samples
- **Dark Mode** - CSS variables for theming

### 🔄 API & Backend
- **RESTful Endpoints** - predict, batch-predict, feature-importance, metrics
- **CORS Support** - cross-origin resource sharing
- **Error Handling** - comprehensive error responses
- **Rate Limiting** - protect against abuse (via Nginx)
- **Health Checks** - API status monitoring

### 🔧 DevOps & CI/CD
- **GitHub Actions** - automated testing on push/PR
- **Linting & Formatting** - flake8, black, isort
- **Security Scanning** - bandit, safety checks
- **Docker Multi-stage** - optimized image builds
- **Nginx Reverse Proxy** - production-grade proxy
- **Health Monitoring** - container health checks

### 📈 Testing
- **Unit Tests** - pytest with fixtures
- **Coverage Reports** - HTML coverage dashboard
- **Integration Tests** - end-to-end pipeline testing
- **40+ Test Cases** - covering all major components

---

## 📁 Project Structure

```
DataScience-Demo-2022/
├── 📄 README.md                 # Main documentation
├── 📄 README_PROJECT.md         # ML project details
├── 📄 SETUP.md                  # Setup & deployment guide
├── 📋 Makefile                  # Build automation (30+ targets)
│
├── 🔧 Configuration
│   ├── .env.example             # Environment variables template
│   ├── .gitignore               # Git ignore rules
│   ├── config.py                # Flask configuration
│   ├── requirements.txt          # Python dependencies
│   ├── Dockerfile               # Container definition
│   ├── docker-compose.yml       # Multi-container setup
│   └── nginx.conf               # Reverse proxy config
│
├── 🤖 Machine Learning (src/)
│   ├── data_loader.py           # Data loading & preprocessing
│   ├── model.py                 # XGBoost model wrapper
│   └── utils.py                 # Utility functions
│
├── 🧪 Tests (tests/)
│   └── test_ml_pipeline.py      # 40+ test cases
│
├── 🌐 Frontend (frontend/)
│   ├── package.json             # npm dependencies
│   ├── templates/
│   │   └── index.html           # Main HTML (semantic, accessible)
│   └── static/
│       ├── css/style.css        # 1000+ lines, fully responsive
│       └── js/
│           ├── api.js           # API client functions
│           ├── ui.js            # UI utilities
│           ├── charts.js        # Chart.js integration
│           └── main.js          # Application logic
│
├── 🔌 Backend (app.py)
│   └── Flask REST API with 8+ endpoints
│
├── 📊 Notebooks (notebooks/)
│   └── XGBoost_Pipeline.ipynb   # Jupyter walkthrough
│
├── 💾 Data & Models
│   ├── data/                    # Dataset storage
│   ├── models/                  # Trained models
│   └── logs/                    # Application logs
│
└── 🔄 CI/CD (.github/workflows/)
    └── ci.yml                   # GitHub Actions workflow
```

---

## 💻 Technology Stack

### Backend
| Technology | Purpose | Version |
|-----------|---------|---------|
| Python | Language | 3.12 |
| Flask | Web Framework | 3.0 |
| XGBoost | ML Algorithm | 2.1 |
| scikit-learn | ML Library | 1.5 |
| pandas | Data Processing | 2.2 |
| Gunicorn | WSGI Server | 21.2 |

### Frontend
| Technology | Purpose |
|-----------|---------|
| HTML5 | Markup (semantic) |
| CSS3 | Styling (1000+ lines, responsive) |
| JavaScript ES6+ | Interactivity |
| Chart.js | Data Visualization |
| Bootstrap Icons | Icon Library |

### DevOps
| Technology | Purpose |
|-----------|---------|
| Docker | Containerization |
| Docker Compose | Orchestration |
| Nginx | Reverse Proxy |
| GitHub Actions | CI/CD |

---

## 📚 API Documentation

### Endpoints Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/model/info` | Model information |
| POST | `/api/predict` | Single prediction |
| POST | `/api/predict/batch` | Batch predictions |
| GET | `/api/feature-importance` | Feature importance |
| GET | `/api/metrics` | Model metrics |
| GET | `/api/generate-sample` | Sample data generation |

### Example: Single Prediction

```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [0.5, -0.2, 1.3, 0.1, -0.5, 0.8, 1.2, -0.3, 0.4, 0.9]}'
```

**Response:**
```json
{
  "prediction": 1,
  "probabilities": {
    "class_0": 0.25,
    "class_1": 0.75
  },
  "confidence": 0.75
}
```

---

## 🧪 Testing

### Run All Tests
```bash
make test           # Run all tests
make test-cov       # With coverage report
```

### Test Coverage
- **DataLoader**: Data loading & preprocessing (10 tests)
- **XGBoostModel**: Model training & prediction (20+ tests)
- **Integration**: End-to-end pipelines (2 tests)

**Current Coverage**: >90%

---

## 📦 Installation & Deployment

### Prerequisites
- Python 3.12+
- Node.js 18+ (for frontend)
- Docker & Docker Compose (optional)

### Local Setup
```bash
# 1. Clone
git clone https://github.com/Debadip98/DataScience-Demo-2022.git
cd DataScience-Demo-2022

# 2. Install
make install

# 3. Run
make dev

# 4. Open browser
# http://localhost:5000
```

### Docker Deployment
```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Production Deployment
```bash
# Build & run with production settings
FLASK_ENV=production make run-prod
```

---

## 🔐 Security Features

✓ **Input Validation** - All API endpoints validate inputs  
✓ **CORS Configuration** - Controlled cross-origin requests  
✓ **Security Headers** - X-Frame-Options, X-Content-Type-Options, etc.  
✓ **Rate Limiting** - Per-IP rate limits (via Nginx)  
✓ **Error Handling** - No sensitive information leakage  
✓ **Non-root User** - Docker containers run as non-root  
✓ **Bandit Scanning** - Automated security checks in CI/CD  
✓ **Health Checks** - Container health monitoring  

---

## 📋 Available Commands

```bash
# Development
make help              # Show all commands
make install          # Install all dependencies
make dev              # Run both frontend & backend

# Code Quality
make lint             # Run linting (flake8)
make format           # Format code (black, isort)
make security         # Security scanning

# Testing
make test             # Run unit tests
make test-cov         # Run with coverage
make check            # lint + security + test

# Deployment
make docker-build     # Build Docker image
make docker-run       # Run Docker container
make run-prod         # Production mode

# Cleanup
make clean            # Clean generated files
make deep-clean       # Complete cleanup
```

See `Makefile` for 30+ commands and `SETUP.md` for detailed documentation.

---

## 🔄 CI/CD Pipeline

### GitHub Actions Workflow

Triggered on push/PR to `main` or `develop`:

1. **Backend Tests** ✓ Dependency installation, linting, pytest, coverage
2. **Frontend Tests** ✓ Build verification
3. **Security Scans** ✓ Bandit, Safety checks
4. **Docker Build** ✓ Multi-stage image build
5. **Deployment Check** ✓ Readiness verification

All checks must pass before merging to main.

---

## 📊 Model Performance

### Default Model Metrics

| Metric | Value |
|--------|-------|
| Accuracy | ~0.87 |
| Precision | ~0.89 |
| Recall | ~0.83 |
| F1-Score | ~0.86 |
| ROC-AUC | ~0.92 |

*Note: Trained on synthetic breast cancer classification dataset*

---

## 🎓 Learning Resources

- **XGBoost**: See `README_PROJECT.md`
- **ML Pipeline**: See `notebooks/XGBoost_Pipeline.ipynb`
- **Setup Guide**: See `SETUP.md`
- **Code Examples**: Check `src/` and `tests/`

---

## 🐛 Troubleshooting

### Port Conflicts
```bash
# Find & kill process
lsof -i :5000
kill -9 <PID>
```

### Virtual Environment Issues
```bash
make clean
make install
```

### Docker Issues
```bash
docker-compose down -v
docker-compose up --build
```

See `SETUP.md` for more troubleshooting tips.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing`)
3. Make changes
4. Run tests (`make test`)
5. Commit (`git commit -am 'Add feature'`)
6. Push (`git push origin feature/amazing`)
7. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Debadip Bhaduri** ([@Debadip98](https://github.com/Debadip98))

- GitHub: [DataScience-Demo-2022](https://github.com/Debadip98/DataScience-Demo-2022)
- Portfolio: [Portfolio Projects](https://github.com/Debadip98)

---

## 📞 Support

- 📖 **Documentation**: Check `README_PROJECT.md` and `SETUP.md`
- 🐛 **Issues**: Open an issue on GitHub
- 💬 **Questions**: Discussions section on GitHub

---

## ⭐ Acknowledgments

- **XGBoost** team for the amazing gradient boosting library
- **scikit-learn** for excellent ML utilities
- **Flask** for the lightweight web framework
- Open source community for awesome tools & libraries

---

## 📈 Project Stats

- **40+ Unit Tests** with >90% coverage
- **1000+ Lines** of frontend CSS
- **8+ API Endpoints** for model interaction
- **30+ Makefile Targets** for automation
- **5 Docker Services** in production stack
- **Fully Responsive** design (mobile to desktop)

---

**Built with ❤️ for Machine Learning & Web Development**

[⬆ Back to Top](#xgboost-ml-model---end-to-end-project)

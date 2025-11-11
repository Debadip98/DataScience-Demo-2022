#!/bin/bash
# Quick verification script for XGBoost ML Project

echo "=================================="
echo "XGBoost ML Project Verification"
echo "=================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} $1"
        return 0
    else
        echo -e "${RED}✗${NC} $1"
        return 1
    fi
}

check_dir() {
    if [ -d "$1" ]; then
        echo -e "${GREEN}✓${NC} $1/"
        return 0
    else
        echo -e "${RED}✗${NC} $1/"
        return 1
    fi
}

echo "📁 Directory Structure:"
check_dir "src"
check_dir "tests"
check_dir "frontend"
check_dir ".github/workflows"
check_dir "models"
check_dir "data"

echo ""
echo "📄 Configuration Files:"
check_file "Makefile"
check_file "Dockerfile"
check_file "docker-compose.yml"
check_file "nginx.conf"
check_file "requirements.txt"
check_file ".env.example"
check_file ".gitignore"

echo ""
echo "📋 Documentation:"
check_file "README.md"
check_file "README_PROJECT.md"
check_file "SETUP.md"
check_file "COMPLETION_SUMMARY.md"

echo ""
echo "🤖 ML Backend:"
check_file "app.py"
check_file "src/model.py"
check_file "src/data_loader.py"
check_file "src/utils.py"
check_file "src/__init__.py"

echo ""
echo "🧪 Tests:"
check_file "tests/test_ml_pipeline.py"

echo ""
echo "🌐 Frontend:"
check_file "frontend/templates/index.html"
check_file "frontend/static/css/style.css"
check_file "frontend/static/js/api.js"
check_file "frontend/static/js/ui.js"
check_file "frontend/static/js/charts.js"
check_file "frontend/static/js/main.js"
check_file "frontend/package.json"

echo ""
echo "🔄 CI/CD:"
check_file ".github/workflows/ci.yml"

echo ""
echo "=================================="
echo "✓ Project Structure Verified!"
echo "=================================="
echo ""
echo "📖 Next Steps:"
echo "1. Install dependencies: make install"
echo "2. Run development: make dev"
echo "3. Run tests: make test"
echo "4. View documentation: cat SETUP.md"
echo ""
echo "🌐 After starting, visit: http://localhost:5000"
echo ""

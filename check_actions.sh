#!/bin/bash

# XGBoost ML Project - GitHub Actions Status Check
# This script monitors the CI/CD pipeline on GitHub

set -e

echo "============================================================================"
echo "XGBoost ML Project - GitHub Actions CI/CD Pipeline"
echo "============================================================================"
echo ""

REPO="Debadip98/DataScience-Demo-2022"
GH_API="https://api.github.com/repos/$REPO"

echo "📋 Repository: $REPO"
echo ""

# Check if gh CLI is available
if ! command -v gh &> /dev/null; then
    echo "⚠️  GitHub CLI (gh) not found. Install it to check workflow status:"
    echo "   https://cli.github.com/manual/installation"
    echo ""
    echo "You can view workflow status at:"
    echo "   https://github.com/$REPO/actions"
    exit 0
fi

# Check authentication
if ! gh auth status &> /dev/null; then
    echo "⚠️  Not authenticated with GitHub. Run:"
    echo "   gh auth login"
    exit 0
fi

echo "🔄 Checking latest workflow runs..."
echo ""

# Get latest workflow runs
gh run list --repo $REPO --limit 5 --json status,conclusion,name,updatedAt,number --template \
'table
{{range .}}
{{.number | printf "%6v"}} | {{.name}} | {{.status}} | {{.conclusion}} | {{.updatedAt}}
{{end}}'

echo ""
echo "✨ Recent Commits:"
gh api repos/$REPO/commits --limit 3 -q '.[] | "\(.sha[0:7]) - \(.commit.message | split("\n")[0]) (\(.author.login // "unknown"))"'

echo ""
echo "============================================================================"
echo "📊 Workflow Status Dashboard"
echo "============================================================================"
echo ""
echo "View full workflow runs at:"
echo "   https://github.com/$REPO/actions"
echo ""
echo "Key workflows:"
echo "   - Backend Testing (Python, pytest, flake8)"
echo "   - Frontend Testing (Node.js, build verification)"
echo "   - Security Scanning (Bandit, Safety)"
echo "   - Docker Build (Multi-stage optimization)"
echo "   - Deployment Check (Readiness verification)"
echo ""

# Get workflow file info
echo "CI/CD Configuration:"
echo "   Workflow File: .github/workflows/ci.yml"
echo "   Trigger Events: push, pull_request"
echo "   Branches: main, develop"
echo ""

# Get latest commit info
LATEST_COMMIT=$(gh api repos/$REPO/commits/main --jq '.sha[0:7]')
LATEST_MESSAGE=$(gh api repos/$REPO/commits/main --jq '.commit.message | split("\n")[0]')

echo "Latest Deployment:"
echo "   Commit: $LATEST_COMMIT"
echo "   Message: $LATEST_MESSAGE"
echo ""
echo "============================================================================"

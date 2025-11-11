# Multi-stage build for XGBoost ML Dashboard
FROM python:3.12-slim as python-builder

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --user --no-cache-dir -r requirements.txt

# ============================================================================
# Final Stage
# ============================================================================

FROM python:3.12-slim

# Install Node.js for frontend
RUN apt-get update && apt-get install -y --no-install-recommends \
    nodejs \
    npm \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy Python dependencies from builder
COPY --from=python-builder /root/.local /root/.local

# Set PATH for pip user installations
ENV PATH=/root/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=app.py \
    FLASK_ENV=production

# Copy entire application
COPY . .

# Install frontend dependencies
WORKDIR /app/frontend
RUN npm install --production

# Return to app directory
WORKDIR /app

# Install gunicorn for production
RUN pip install --user --no-cache-dir gunicorn

# Create non-root user for security
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose ports
EXPOSE 5000 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/api/health || exit 1

# Start application
CMD ["sh", "-c", "python app.py"]

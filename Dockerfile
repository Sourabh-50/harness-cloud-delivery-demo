# Security-hardened minimal base image
FROM python:3.11-slim

# Prevent Python from writing pyc files and buffer outputs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5000

WORKDIR /app

# Install dependencies separately to leverage layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY app/ ./app/

# Security Hardening: Create non-root system user and group
RUN groupadd -g 10001 appgroup && \
    useradd -u 10001 -g appgroup -m -s /bin/false appuser && \
    chown -R appuser:appgroup /app /home/appuser

# Switch to non-root user
USER appuser

EXPOSE 5000

# Production WSGI Server launch
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app.app:app"]

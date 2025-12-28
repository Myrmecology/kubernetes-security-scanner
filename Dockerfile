# Kubernetes Security Scanner - Docker Image
# This allows the scanner to run in a containerized environment

FROM python:3.11-slim

# Metadata
LABEL maintainer="your.email@example.com"
LABEL description="Kubernetes Security Scanner - Identify cluster misconfigurations"
LABEL version="1.0.0"

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install kubectl
RUN curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" \
    && chmod +x kubectl \
    && mv kubectl /usr/local/bin/

# Copy requirements first for better layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY setup.py .
COPY README.md .

# Install the package
RUN pip install -e .

# Create non-root user for security
RUN useradd -m -u 1000 scanner && \
    chown -R scanner:scanner /app

# Switch to non-root user
USER scanner

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Default command
ENTRYPOINT ["python", "-m", "src.scanner"]
CMD ["--help"]

# Usage examples:
# Build: docker build -t k8s-security-scanner .
# Run: docker run --rm -v ~/.kube:/home/scanner/.kube:ro k8s-security-scanner
# Scan: docker run --rm -v ~/.kube:/home/scanner/.kube:ro k8s-security-scanner --namespace default
# Multi-stage build dengan optimasi

# Stage 1: Builder
FROM python:3.11-slim as builder

WORKDIR /app

# Copy hanya requirements.txt dulu (caching layer)
COPY requirements.txt .

# Install dependencies dengan pip cache
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Final
FROM python:3.11-slim

WORKDIR /app

# Install runtime system dependencies (minimal)
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY . .

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Create necessary directories
RUN mkdir -p logs memory_storage backups

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1

# Expose ports
EXPOSE 8080 8765 9090

# Run bot
CMD ["python", "main.py"]

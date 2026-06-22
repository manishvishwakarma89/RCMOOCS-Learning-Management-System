# Stage 1: Builder
FROM python:3.11-slim AS builder

WORKDIR /app

# Install system dependencies for psycopg2
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --target=/app/deps

# Copy application code
COPY . .


# Stage 2: Runner — must match builder's base (slim/glibc, not alpine/musl)
FROM python:3.11-slim AS runner

WORKDIR /app

# Install libpq runtime library (psycopg2 needs it at runtime)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copy installed dependencies from builder
COPY --from=builder /app/deps ./deps

# Copy application files
COPY --from=builder /app/app.py .
COPY --from=builder /app/models.py .
COPY --from=builder /app/static ./static
COPY --from=builder /app/templates ./templates

ENV PYTHONPATH="/app/deps"
ENV PYTHON_ENV=production
ENV PORT=5000

EXPOSE 5000

CMD ["python", "app.py"]

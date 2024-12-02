FROM python:3.12.3-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN python -m pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Set the working directory
WORKDIR /app
COPY . /app

# Set permissions and use non-root user
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# Default command
CMD ["python", "main.py"]

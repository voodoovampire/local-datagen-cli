FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create .env from example if not exists
RUN cp .env.example .env 2>/dev/null || true

# Expose port if needed
# EXPOSE 8000

# Run the application
CMD ["python", "main.py"]

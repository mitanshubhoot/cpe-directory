# Official Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY backend/requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy entire backend and frontend_build
COPY backend/ .

# Expose the port used by Flask
EXPOSE 5000

# Run the Flask app via Gunicorn
CMD ["gunicorn", "api:app", "--bind", "0.0.0.0:5000", "--workers", "1", "--threads", "2", "--timeout", "90"]

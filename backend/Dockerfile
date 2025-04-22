# Use the official Python 3.13.1 slim image as the base
FROM python:3.13.1-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libffi-dev \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install pipenv or use requirements.txt
# COPY Pipfile Pipfile.lock ./
# RUN pip install pipenv && pipenv install --deploy --system

# Alternatively, use requirements.txt
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the application code
COPY . .

# Expose the port FastAPI will run on
EXPOSE 8000

# Command to run the application using Uvicorn
CMD ["python", "main.py"]

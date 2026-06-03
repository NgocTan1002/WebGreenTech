# Base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements/ /app/requirements/
RUN pip install --upgrade pip
RUN pip install -r requirements/dev.txt

# Copy project
COPY . /app/

# Expose port
EXPOSE 8000

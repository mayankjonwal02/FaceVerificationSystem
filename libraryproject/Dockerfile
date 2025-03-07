# Use the official Python slim base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy requirements.txt to the working directory
COPY requirements.txt .

# Install system dependencies (including MongoDB client tools, dlib dependencies)
RUN apt-get update && \
    apt-get install -y \
    wget \
    gnupg \
    gcc \
    g++ \
    cmake \
    libmariadb-dev-compat \
    libmariadb-dev \
    pkg-config \
    libgl1-mesa-dev \
    libglib2.0-0 \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libboost-python-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Add MongoDB official GPG key and repository
RUN wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | apt-key add - && \
    echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/debian buster/mongodb-org/6.0 main" | tee /etc/apt/sources.list.d/mongodb-org-6.0.list && \
    apt-get update && \
    apt-get install -y mongodb-mongosh && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies (including dlib and pymongo)
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir dlib pymongo

# Copy the rest of the application code
COPY . .

# Expose the application port
EXPOSE 8000

# Define the default command
CMD ["python", "manage.py", "runsslserver", "0.0.0.0:8000"]

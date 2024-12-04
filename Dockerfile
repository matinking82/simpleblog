# Use the official Python base image
FROM python:3.12-slim

# Install necessary packages
RUN apt-get update - && apt-get install -y \
    python3-dev \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config

# Set the working directory in the container
WORKDIR /app

# Copy the application code to the container
COPY . .

# Copy the requirements file to the container
# COPY requirements.txt .

# Install the Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install mysqlclient

# Start the FastAPI application
CMD ["fastapi", "run", "main.py", "--host", "127.0.0.1", "--port", "8000"]

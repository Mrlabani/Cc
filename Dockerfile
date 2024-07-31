# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set environment variables to ensure Python outputs logs and errors to stdout/stderr
ENV PYTHONUNBUFFERED=1

# Create and set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY . .

# Specify the command to run the application
CMD ["python", "main.py"]

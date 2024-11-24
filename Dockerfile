# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Copy application code and model files to the container
COPY app/ ./app

# Install Python dependencies
RUN pip install --no-cache-dir -r ./app/requirements.txt

# Expose the Flask port
EXPOSE 8080

# Run the application
CMD ["python", "./app/app.py"]

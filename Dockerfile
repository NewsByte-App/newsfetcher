# Use the official Python base image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the requirements
RUN pip install --default-timeout=10000 -r requirements.txt

# First, copy only the necessary files to avoid invalidating the cache unnecessarily
# Ensure your model_data directory is at the root of your project next to the Dockerfile
# Copy the rest of the application code to the working directory
# This is done after installing requirements to leverage Docker cache for faster builds
COPY . .

# Expose the port that the FastAPI application will run on
EXPOSE 8000

# Start the FastAPI application using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Use the official Python image as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install FastAPI, Motor, and Uvicorn
RUN pip install fastapi motor uvicorn

# Copy your FastAPI application code into the container
COPY app.py .

# Expose port 8000 for the FastAPI application
EXPOSE 8000

# Command to run the FastAPI application using Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

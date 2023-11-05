# Use the official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy to docker cache
COPY ./requirements.txt /app/requirements.txt

# Copy the current directory contents into the container at /app
COPY ./src /app/src

# Install any needed packages specified in requirements.txt
# RUN pip install -r requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt


# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]

# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 12345 available to the world outside this container
EXPOSE 12345

# Define environment variable
ENV CONFIG_PATH=/app/config.yml

# Run whisper when the container launches
ENTRYPOINT ["python", "-m", "src.server", "--config", "/app/config.yml"]
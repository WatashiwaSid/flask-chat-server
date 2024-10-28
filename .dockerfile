# Use the official Ubuntu base image
FROM ubuntu:20.04

# Set environment variables to prevent user prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# Update and install system dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-dev && \
    apt-get clean

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements to the working directory
COPY requirements.txt requirements.txt

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the entire project to the container
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Set environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_ENV=development

# Run the Flask application using SocketIO
CMD ["flask", "run", "--host=0.0.0.0"]

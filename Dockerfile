# Use the official Python image as a base image
FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu20.04

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Install Python and other dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy requirements.txt before other files to utilize Docker cache
COPY requirements.txt /app/

# Install Python dependencies
RUN pip3 install --upgrade pip && \
    pip3 install -r requirements.txt

# Copy the rest of the application code
COPY . /app

# Expose ports for gRPC and HTTP servers (change if necessary)
EXPOSE 50051 8080

# Entry point to run your application
# Adjust the command as necessary for your application
CMD ["python3", "server/main.py"]

# If you have a different entry point, you can specify it here
# CMD ["python3", "scripts/train_model.py"]

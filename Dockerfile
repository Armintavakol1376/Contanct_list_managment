# Use Ubuntu as the base image
FROM ubuntu:22.04

# Set environment variables to avoid interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install Python and MySQL dependencies (including pkg-config)
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv \
    default-libmysqlclient-dev pkg-config build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create a working directory
WORKDIR /app

# Copy requirements file first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose port if your Flask app uses one (e.g., 5000)
EXPOSE 5000

# Command to run your application
CMD ["python3", "app.py"]
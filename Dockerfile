# Use Python 3.11 with proper OpenSSL support
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for SSL and certs
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libssl-dev ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source code
COPY src/ ./src/

# Expose port
EXPOSE 8000

# Run the app
CMD ["python", "src/app.py"]

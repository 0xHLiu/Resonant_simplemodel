FROM python:3.10-slim

# Install system dependencies for ffprobe
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY app.py .
COPY start.sh .

# Make startup script executable
RUN chmod +x start.sh

# Create output folder
RUN mkdir -p output

# Expose port
EXPOSE 8001

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["./start.sh"]

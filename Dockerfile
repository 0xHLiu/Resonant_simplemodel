FROM python:3.10-slim

# Create app directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY app.py .

# Create output folder
RUN mkdir -p output

# Set default command
ENTRYPOINT ["python", "app.py"]

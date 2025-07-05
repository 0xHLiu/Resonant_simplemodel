# Docker Setup for Text-to-Speech API

This repository can be run as a persistent Docker container that handles HTTP requests on port 8001.

## Prerequisites

- Docker installed on your system
- Docker Compose (usually comes with Docker Desktop)
- OpenAI API key

## Quick Start

### 1. Set Environment Variables

Create a `.env` file in the project root:

```bash
OPENAI_API_KEY=your_openai_api_key_here
AGGREGATOR_URL=https://aggregator.walrus-testnet.walrus.space
```

### 2. Build and Run with Docker Compose (Recommended)

```bash
# Build and start the container
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the container
docker-compose down
```

### 3. Build and Run with Docker Commands

```bash
# Build the image
docker build -t tts-api .

# Run the container
docker run -d \
  --name tts-api \
  -p 8001:8001 \
  -e OPENAI_API_KEY=your_openai_api_key_here \
  -e AGGREGATOR_URL=https://aggregator.walrus-testnet.walrus.space \
  -v $(pwd)/output:/app/output \
  --restart unless-stopped \
  tts-api
```

## Container Features

- **Persistent**: Container runs continuously and restarts automatically
- **Health Check**: Monitors API health every 30 seconds
- **Volume Mounting**: Output directory is mounted for file persistence
- **Environment Variables**: Configurable via environment variables
- **Port Exposure**: API accessible on port 8001

## API Endpoints

Once the container is running, you can access:

- **Health Check**: `GET http://localhost:8001/health`
- **API Info**: `GET http://localhost:8001/`
- **Text-to-Speech**: `POST http://localhost:8001/tts/download`

## Example Usage

```bash
# Test the API
curl -X POST "http://localhost:8001/tts/download" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello, this is a test!",
    "storage_id": "emHbGOU2cXUN3g-okz0FF4QDWhlhLQmDcPlZwZd2Ark",
    "voice": "alloy"
  }' \
  --output speech.mp3
```

## Container Management

```bash
# View running containers
docker ps

# View logs
docker logs tts-api

# Stop container
docker stop tts-api

# Start container
docker start tts-api

# Remove container
docker rm tts-api

# Remove image
docker rmi tts-api
```

## Troubleshooting

### Container won't start
- Check if port 8001 is available
- Verify environment variables are set correctly
- Check Docker logs: `docker logs tts-api`

### API not responding
- Ensure container is running: `docker ps`
- Check health endpoint: `curl http://localhost:8001/health`
- Verify OpenAI API key is valid

### File permissions
- The output directory is mounted as a volume
- Files are automatically cleaned up after 5 seconds
- Check volume permissions if needed

## Production Deployment

For production deployment:

1. Use a reverse proxy (nginx, traefik)
2. Set up SSL/TLS certificates
3. Use Docker secrets for API keys
4. Configure proper logging
5. Set up monitoring and alerting 
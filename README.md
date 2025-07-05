# Text-to-Speech API

A FastAPI-based backend service that converts text to speech using OpenAI's TTS API.

## Features

- Convert text to speech using OpenAI's TTS models
- Multiple voice options (alloy, echo, fable, etc.)
- Direct file download or file path response
- RESTful API with automatic documentation
- Health check endpoint
- Input validation and error handling

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up your OpenAI API key:**
   ```bash
   export OPENAI_API_KEY="your-openai-api-key-here"
   ```

3. **Run the server:**
   ```bash
   python app.py
   ```

The server will start on `http://localhost:8000`

## API Endpoints

### 1. Root Endpoint
- **GET** `/`
- Returns API information and available endpoints

### 2. Health Check
- **GET** `/health`
- Returns the health status of the API

### 3. Text-to-Speech (with file path response)
- **POST** `/tts`
- Converts text to speech and returns file information
- **Request Body:**
  ```json
  {
    "text": "Hello, world!",
    "voice": "alloy",
    "model": "tts-1"
  }
  ```
- **Response:**
  ```json
  {
    "message": "Audio generated successfully",
    "file_path": "output/uuid.mp3"
  }
  ```

### 4. Direct Download
- **POST** `/tts/download`
- Converts text to speech and returns the MP3 file directly
- **Request Body:** Same as `/tts`
- **Response:** MP3 audio file for download

### 5. Download by File ID
- **GET** `/download/{file_id}`
- Downloads a previously generated audio file by its UUID

## Available Voices

- `alloy` (default)
- `echo`
- `fable`
- `onyx`
- `nova`
- `shimmer`

## Available Models

- `tts-1` (default)
- `tts-1-hd`
- `gpt-4o-mini-tts`

## Usage Examples

### Using curl

1. **Convert text to speech:**
   ```bash
   curl -X POST "http://localhost:8000/tts" \
        -H "Content-Type: application/json" \
        -d '{"text": "Hello, this is a test!", "voice": "alloy"}'
   ```

2. **Download audio directly:**
   ```bash
   curl -X POST "http://localhost:8000/tts/download" \
        -H "Content-Type: application/json" \
        -d '{"text": "Hello, this is a test!", "voice": "echo"}' \
        --output speech.mp3
   ```

### Using Python

```python
import requests

# Convert text to speech
response = requests.post("http://localhost:8000/tts", json={
    "text": "Hello, world!",
    "voice": "alloy",
    "model": "tts-1"
})

print(response.json())

# Download audio directly
response = requests.post("http://localhost:8000/tts/download", json={
    "text": "Hello, world!",
    "voice": "echo"
})

with open("speech.mp3", "wb") as f:
    f.write(response.content)
```

## Testing

Run the test script to verify the API is working:

```bash
python test_api.py
```

## API Documentation

Once the server is running, you can access:
- **Interactive API docs:** http://localhost:8000/docs
- **ReDoc documentation:** http://localhost:8000/redoc

## Docker Support

The project includes a Dockerfile for containerized deployment:

```bash
# Build the image
docker build -t tts-api .

# Run the container
docker run -p 8000:8000 -e OPENAI_API_KEY="your-key" tts-api
```

## Error Handling

The API includes comprehensive error handling:
- **400 Bad Request:** Invalid input (empty text, invalid voice/model)
- **404 Not Found:** Requested audio file doesn't exist
- **500 Internal Server Error:** OpenAI API errors or file system issues

## File Management

- Generated audio files are stored in the `output/` directory
- Each file is named with a unique UUID
- Files persist between API calls for download access

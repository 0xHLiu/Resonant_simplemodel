import os
import uuid
import tempfile
import requests
import subprocess
from pathlib import Path
from typing import Optional

import openai
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel


# Initialize OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize FastAPI app
app = FastAPI(
    title="Text-to-Speech API",
    description="Convert text to speech using OpenAI's TTS API",
    version="1.0.0"
)

# Create output directory
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

# Configuration for external model parameter service
MODEL_PARAMS_URL = os.getenv("MODEL_PARAMS_URL", "https://api.example.com/model-params")

def validate_mp3_file(file_path: Path) -> bool:
    """
    Validate that an MP3 file is playable
    
    Args:
        file_path: Path to the MP3 file
        
    Returns:
        bool: True if file is valid and playable, False otherwise
    """
    try:
        # Check if file exists and has content
        if not file_path.exists() or file_path.stat().st_size == 0:
            return False
        
        # Use ffprobe to check if the file is a valid audio file
        result = subprocess.run(
            ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", str(file_path)],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        # If ffprobe succeeds, the file is valid
        return result.returncode == 0
        
    except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
        # If ffprobe is not available or fails, try a basic file check
        try:
            # Check if file starts with MP3 header or has reasonable size
            with open(file_path, 'rb') as f:
                header = f.read(10)
                # Check for MP3 sync bytes (0xFF 0xFB or 0xFF 0xF3)
                if len(header) >= 2 and header[0] == 0xFF and header[1] in [0xFB, 0xF3]:
                    return True
                # If no MP3 header, check if file is reasonably sized (> 1KB)
                if file_path.stat().st_size > 1024:
                    return True
            return False
        except Exception:
            return False

async def fetch_model_parameters(storage_id: str) -> dict:
    """
    Fetch model parameters from external service using storage_id
    
    Args:
        storage_id: The storage ID to fetch parameters for
        
    Returns:
        dict: Model parameters from the external service
        
    Raises:
        HTTPException: If the external service request fails
    """
    # If no MODEL_PARAMS_URL is set, return empty dict (bypass external service)
    if MODEL_PARAMS_URL == "https://api.example.com/model-params":
        return {}
    
    try:
        response = requests.post(
            MODEL_PARAMS_URL,
            json={"storage_id": storage_id},
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to fetch model parameters: {str(e)}"
        )

class TextToSpeechRequest(BaseModel):
    text: str
    storage_id: str
    voice: str = "alloy"  # Default voice

class TextToSpeechResponse(BaseModel):
    message: str
    file_path: str

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Text-to-Speech API",
        "version": "1.0.0",
        "endpoints": {
            "POST /tts": "Convert text to speech (returns file info)",
            "POST /tts/download": "Convert text to speech (returns MP3 file)",
            "GET /download/{file_id}": "Download audio file by ID",
            "GET /health": "Health check"
        },
        "required_fields": {
            "text": "The text to convert to speech",
            "storage_id": "ID to fetch model parameters from external service"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "API is running"}

@app.post("/tts", response_model=TextToSpeechResponse)
async def text_to_speech(request: TextToSpeechRequest):
    """
    Convert text to speech and return the audio file
    
    Args:
        request: TextToSpeechRequest containing text, storage_id, and voice
        
    Returns:
        TextToSpeechResponse: Response with success message and file path
    """
    try:
        # Validate input
        if not request.text.strip():
            raise HTTPException(status_code=400, detail="Text cannot be empty")
        if not request.storage_id.strip():
            raise HTTPException(status_code=400, detail="Storage ID cannot be empty")
        
        # Fetch model parameters from external service
        model_params = await fetch_model_parameters(request.storage_id)
        
        # Generate unique filename
        file_id = str(uuid.uuid4())
        output_path = OUTPUT_DIR / f"{file_id}.mp3"
        
        # Call OpenAI TTS API with hardcoded model
        response = openai.audio.speech.create(
            model="tts-1",
            voice=request.voice,
            input=request.text
        )
        
        # Save the audio file
        with open(output_path, "wb") as f:
            f.write(response.read())
        
        # Validate the generated MP3 file
        if not validate_mp3_file(output_path):
            # Clean up the invalid file
            output_path.unlink(missing_ok=True)
            raise HTTPException(
                status_code=500, 
                detail="Generated audio file is not playable. Please try again."
            )
        
        return TextToSpeechResponse(
            message="Audio generated successfully",
            file_path=str(output_path)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating audio: {str(e)}")

@app.get("/download/{file_id}")
async def download_audio(file_id: str):
    """
    Download the generated audio file
    
    Args:
        file_id: The UUID of the generated file
        
    Returns:
        FileResponse: MP3 audio file
    """
    file_path = OUTPUT_DIR / f"{file_id}.mp3"
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Audio file not found")
    
    return FileResponse(
        path=file_path,
        media_type="audio/mpeg",
        filename=f"{file_id}.mp3"
    )

@app.post("/tts/download")
async def text_to_speech_download(request: TextToSpeechRequest):
    """
    Convert text to speech and directly return the audio file for download
    
    Args:
        request: TextToSpeechRequest containing text, storage_id, and voice
        
    Returns:
        FileResponse: MP3 audio file for direct download
    """
    try:
        # Validate input
        if not request.text.strip():
            raise HTTPException(status_code=400, detail="Text cannot be empty")
        if not request.storage_id.strip():
            raise HTTPException(status_code=400, detail="Storage ID cannot be empty")
        
        # Fetch model parameters from external service
        model_params = await fetch_model_parameters(request.storage_id)
        
        # Generate unique filename
        file_id = str(uuid.uuid4())
        output_path = OUTPUT_DIR / f"{file_id}.mp3"
        
        # Call OpenAI TTS API with hardcoded model
        response = openai.audio.speech.create(
            model="tts-1",
            voice=request.voice,
            input=request.text
        )
        
        # Save the audio file
        with open(output_path, "wb") as f:
            f.write(response.read())
        
        # Validate the generated MP3 file
        if not validate_mp3_file(output_path):
            # Clean up the invalid file
            output_path.unlink(missing_ok=True)
            raise HTTPException(
                status_code=500, 
                detail="Generated audio file is not playable. Please try again."
            )
        
        # Return the file directly for download
        return FileResponse(
            path=output_path,
            media_type="audio/mpeg",
            filename=f"speech_{file_id}.mp3"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating audio: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

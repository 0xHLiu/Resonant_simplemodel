import os
import uuid
import tempfile
import requests
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

class TextToSpeechRequest(BaseModel):
    text: str
    voice: str = "alloy"  # Default voice
    model: str = "tts-1"  # Default model

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
            "POST /tts": "Convert text to speech",
            "GET /health": "Health check"
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
        request: TextToSpeechRequest containing text, voice, and model
        
    Returns:
        FileResponse: MP3 audio file
    """
    try:
        # Validate input
        if not request.text.strip():
            raise HTTPException(status_code=400, detail="Text cannot be empty")
        
        # Generate unique filename
        file_id = str(uuid.uuid4())
        output_path = OUTPUT_DIR / f"{file_id}.mp3"
        
        # Call OpenAI TTS API
        response = openai.audio.speech.create(
            model=request.model,
            voice=request.voice,
            input=request.text
        )
        
        # Save the audio file
        with open(output_path, "wb") as f:
            f.write(response.read())
        
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
        request: TextToSpeechRequest containing text, voice, and model
        
    Returns:
        FileResponse: MP3 audio file for direct download
    """
    try:
        # Validate input
        if not request.text.strip():
            raise HTTPException(status_code=400, detail="Text cannot be empty")
        
        # Generate unique filename
        file_id = str(uuid.uuid4())
        output_path = OUTPUT_DIR / f"{file_id}.mp3"
        
        # Call OpenAI TTS API
        response = openai.audio.speech.create(
            model=request.model,
            voice=request.voice,
            input=request.text
        )
        
        # Save the audio file
        with open(output_path, "wb") as f:
            f.write(response.read())
        
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
    uvicorn.run(app, host="0.0.0.0", port=8000)

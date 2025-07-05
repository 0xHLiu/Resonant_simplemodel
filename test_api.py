#!/usr/bin/env python3
"""
Test script for the Text-to-Speech FastAPI service
"""

import requests
import json

# API base URL
BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint"""
    print("Testing health check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_text_to_speech():
    """Test the text-to-speech endpoint"""
    print("Testing text-to-speech...")
    
    # Test data
    data = {
        "text": "Hello, this is a test of the text-to-speech API!",
        "voice": "alloy",
        "model": "tts-1"
    }
    
    response = requests.post(f"{BASE_URL}/tts", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_direct_download():
    """Test the direct download endpoint"""
    print("Testing direct download...")
    
    # Test data
    data = {
        "text": "This audio will be downloaded directly!",
        "voice": "echo",
        "model": "tts-1"
    }
    
    response = requests.post(f"{BASE_URL}/tts/download", json=data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        # Save the audio file
        filename = "test_download.mp3"
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"Audio saved as: {filename}")
    else:
        print(f"Error: {response.text}")
    print()

def test_root_endpoint():
    """Test the root endpoint"""
    print("Testing root endpoint...")
    response = requests.get(BASE_URL)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

if __name__ == "__main__":
    print("Testing Text-to-Speech FastAPI Service")
    print("=" * 40)
    
    try:
        test_root_endpoint()
        test_health_check()
        test_text_to_speech()
        test_direct_download()
        
        print("All tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API server.")
        print("Make sure the server is running with: python app.py")
    except Exception as e:
        print(f"Error: {e}") 
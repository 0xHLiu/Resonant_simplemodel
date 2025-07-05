#!/usr/bin/env python3
"""
Test script for the Text-to-Speech FastAPI service
"""

import requests
import os

# API base URL (update to match your server port)
BASE_URL = "http://localhost:8001"

# List to keep track of files to clean up
test_files = []

def test_health_check():
    """Test the health check endpoint"""
    print("Testing health check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_direct_download():
    """Test the direct download endpoint"""
    print("Testing direct download...")

    # Use the known working storage_id
    data = {
        "text": "This audio will be downloaded directly!",
        "storage_id": "emHbGOU2cXUN3g-okz0FF4QDWhlhLQmDcPlZwZd2Ark",
        "voice": "echo"
    }

    response = requests.post(f"{BASE_URL}/tts/download", json=data)
    print(f"Status: {response.status_code}")

    if response.status_code == 200:
        filename = "test_download.mp3"
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"Audio saved as: {filename}")
        test_files.append(filename)
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

def cleanup():
    """Delete any test files created during the run."""
    print("Cleaning up test files...")
    for filename in test_files:
        try:
            os.remove(filename)
            print(f"Deleted: {filename}")
        except Exception as e:
            print(f"Could not delete {filename}: {e}")

if __name__ == "__main__":
    print("Testing Text-to-Speech FastAPI Service")
    print("=" * 40)

    try:
        test_root_endpoint()
        test_health_check()
        test_direct_download()
        print("All tests completed!")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API server.")
        print("Make sure the server is running with: python app.py")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cleanup()
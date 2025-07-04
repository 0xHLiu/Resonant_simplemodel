import sys
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def text_to_speech(text, output_path="output/output.mp3"):
    response = openai.audio.speech.create(
        model="tts-1",
        voice="alloy",  # or echo, fable, etc.
        input=text
    )
    with open(output_path, "wb") as f:
        f.write(response.read())
    print(f"Audio saved to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python app.py \"Your text here\"")
        sys.exit(1)
    os.makedirs("output", exist_ok=True)
    input_text = sys.argv[1]
    text_to_speech(input_text)

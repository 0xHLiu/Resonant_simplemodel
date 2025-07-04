# Resonant_simplemodel
Simplistic voice model to dockerize and test Oasis Protocol

Steps:
0. export OPENAI_API_KEY=<INPUT>
1. docker build -t tts-app .
2. docker run --rm -e OPENAI_API_KEY=$OPENAI_API_KEY -v $(pwd)/output:/app/output tts-app "Hello, this is a test"

Container Set Up:
1. export PAT=<INPUT>
2. echo $PAT | docker login ghcr.io -u USERNAME --password-stdin
3. docker build -t ghcr.io/0xhliu/tts-docker-app:latest .
4. docker push ghcr.io/0xhliu/tts-docker-app:latest
5. docker run --rm \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  -v $(pwd)/output:/app/output \
  ghcr.io/0xhliu/tts-docker-app:latest "Text to convert"

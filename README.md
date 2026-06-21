# MyKare AI LiveKit Assistant

This repository contains a Python-based LiveKit voice assistant application.

## Requirements

- Docker
- A `.env` file at the repository root with your environment variables:
  - `LIVEKIT_URL`
  - `LIVEKIT_API_KEY`
  - `LIVEKIT_API_SECRET`
  - `MONGO_URI`
  - `OPENAI_API_KEY`
  - `TAVUS_API_KEY`
  - `DEEPGRAM_API_KEY`
  - `CARTESIA_API_KEY`
  - `AGENT_MODEL` (optional)

## Build Docker image

From the repository root:

```bash
docker build -t mykare-livekit .
```

## Run in Docker

```bash
docker run --rm -p 8000:8000 \
  --env-file .env \
  mykare-livekit
```

## Run locally

Install dependencies in a Python environment:

```bash
python -m pip install -r requirements.txt
```

Then run:

```bash
python main.py start
```

## Notes

- `main.py` already prints `LIVEKIT_URL`, `LIVEKIT_API_KEY`, and `LIVEKIT_API_SECRET` on startup.
- If your app uses MongoDB, make sure `MONGO_URI` is reachable from the container or local environment.
- Adjust exposed ports and environment variables as needed for your LiveKit deployment.

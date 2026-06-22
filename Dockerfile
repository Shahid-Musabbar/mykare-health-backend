FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies needed by some Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    # libffi-dev \
    # libsndfile1 \
    # libportaudio2 \
    # ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy the application files and dependencies list
COPY requirements.txt ./
COPY main.py ./
COPY agent.py ./
# COPY .env ./

# Install Python dependencies
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Expose ports if needed by the app or LiveKit
# EXPOSE 8000

CMD ["python", "main.py", "start"]

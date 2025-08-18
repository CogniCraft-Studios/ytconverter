FROM python:3.9-slim-bullseye

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install yt-dlp and ffmpeg
RUN apt-get update && apt-get install -y ffmpeg
RUN pip install yt-dlp==2025.8.11

COPY . .
RUN mkdir -p downloads

EXPOSE 5005

CMD ["python", "app.py"]
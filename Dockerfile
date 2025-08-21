FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg ca-certificates && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir yt-dlp==2025.8.11

COPY . .

# Copy entrypoint after ".", ensure LF & exec bit
COPY entrypoint.sh /entrypoint.sh
# strip possible CRLFs (works on Debian slim)
RUN sed -i 's/\r$//' /entrypoint.sh && chmod +x /entrypoint.sh

RUN mkdir -p downloads
EXPOSE 5005

# Call via /bin/sh to avoid shebang issues on some runtimes
ENTRYPOINT ["/bin/sh", "/entrypoint.sh"]
CMD ["python", "app.py"]

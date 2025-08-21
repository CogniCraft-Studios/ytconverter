# YT2MP34 - YouTube to MP3/MP4 Converter

This project provides a web application to convert YouTube videos to MP3 or MP4 formats, along with a cookie refreshing service and a download cleaner.

## Applications and Their Roles

### 1. `app` (Main Web Application)

- **Description**: This is the core Flask web application that provides the user interface for converting YouTube videos. Users can paste a YouTube URL, and the application will process the video and provide download links for MP3 or MP4.
- **Role in System**: Serves as the primary interface for users to interact with the service.
- **Usage**: Accessible via a web browser after deployment.

### 2. `cleaner` (Download Cleaner)

- **Description**: A background service responsible for cleaning up old downloaded files from the `downloads/` directory.
- **Role in System**: Ensures that the storage space is managed efficiently by removing temporary or outdated files.
- **Usage**: Runs periodically as configured in `docker-compose.yml`.

### 3. `cookie-refresher` (Cookie Refreshing Service)

- **Description**: A service that periodically refreshes YouTube authentication cookies. These cookies are essential for bypassing certain YouTube restrictions and ensuring successful video downloads.
- **Role in System**: Maintains valid authentication sessions with YouTube to enable uninterrupted video processing by the `app`.
- **Usage**: Designed to be run as a scheduled task (e.g., weekly cron job in environments like Coolify).

## Installation and Setup

To set up and run this project, follow these steps:

1.  **Clone the repository**:

    ```bash
    git clone <repository_url>
    cd yt2mp34
    ```

2.  **Build and run with Docker Compose**:

    ```bash
    docker-compose up --build -d
    ```

    This command will:

    - Build the Docker images for `app`, `cleaner`, and `cookie-refresher`.
    - Start all services in detached mode.
    - Create a shared volume `cookies-vol` for cookie management.

3.  **Access the application**:
    The `app` service will be accessible at `http://localhost:5005` (or the port you've configured).

## Cookie initial creation and usage

```bash
# build image locally :
docker build -t cookie_refresher .
# run a container using that image :
docker run -it --rm -v $(pwd)/cookies:/tmp --entrypoint bash cookie_refresher
# run command to generate cookies.txt file
python /app/refresh_cookies.py --no-headless
# move cookies.txt from /app folder to /tmp folder
# exit container
# make the cookies.txt file secure met base 64 :
base64 -i cookies.txt > cookies.txt.b64
# use that as an env var in coolify with the name YT2MP3COOKIES_TXT_B64
# this will be picked up by the entrypoint.sh script and put in a cookies.txt file.
# the cookies.txt file will be used by the app to download the videos.
```

In Coolify, the `refresh_cookies.py` script will run each week and create a new cookie overwriting the previous one.
This cookie will be used by the app to download the videos.

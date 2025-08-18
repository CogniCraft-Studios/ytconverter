import os
import subprocess
import re
from flask import Flask, request, jsonify, send_from_directory
import uuid

app = Flask(__name__)

def youtube_download(mp3_filepath="", url=""):
    # delete file if it exists
    if os.path.exists(mp3_filepath):
        os.remove(mp3_filepath)
    # Download audio using yt-dlp
    subprocess.run(
        [
            "yt-dlp",
            url,
            "--no-overwrites",
            "-x",
            "--audio-format",
            "mp3",
            "-o",
            f"{mp3_filepath}",
        ]
    )
    return mp3_filepath

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    file_format = request.form['format']
    bitrate = request.form.get('bitrate', '128K') # Default to 128K if not specified

    # Get video title
    try:
        title_command = [
            'yt-dlp',
            '--get-title',
            url
        ]
        video_title = subprocess.check_output(title_command, text=True, stderr=subprocess.PIPE).strip()
        # Sanitize title for filename: remove special characters and spaces, replace with underscores
        sanitized_title = re.sub(r'[^a-zA-Z0-9_]', '', video_title.replace(' ', '_'))
        # Truncate to first 20 characters
        filename_base = sanitized_title[:20]
    except subprocess.CalledProcessError as e:
        print(f"Error getting title: {e.stderr}")
        filename_base = "video"

    # Ensure download directory exists
    download_dir = os.path.join(os.getcwd(), 'downloads')
    os.makedirs(download_dir, exist_ok=True)

    unique_filename = f"{filename_base}_{uuid.uuid4().hex}.{file_format}"
    output_filepath = os.path.join(download_dir, unique_filename)

    try:
        if file_format == 'mp3':
            # yt-dlp command for MP3 with bitrate
            command = [
                "yt-dlp",
                url,
                "--no-overwrites",
                "-x",
                "--audio-format",
                "mp3",
                "--audio-quality",
                bitrate,
                "-o",
                output_filepath
            ]
        elif file_format == 'mp4':
            # yt-dlp command for MP4
            command = [
                "yt-dlp",
                url,
                "--no-overwrites",
                "-f",
                "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
                "-o",
                output_filepath
            ]
        else:
            return jsonify({'status': 'error', 'message': 'Invalid format specified.'}), 400

        subprocess.run(command, check=True)
        return jsonify({'status': 'success', 'message': 'Download complete!', 'filepath': output_filename})
    except subprocess.CalledProcessError as e:
        return jsonify({'status': 'error', 'message': f'Download failed: {e}'}), 500
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'An unexpected error occurred: {e}'}), 500

@app.route('/download/<filename>')
def download_file(filename):
    download_dir = os.path.join(os.getcwd(), 'downloads')
    return send_from_directory(download_dir, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)
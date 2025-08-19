import os
import time

def cleanup_downloads(directory, age_minutes):
    now = time.time()
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            # Get file modification time
            mod_time = os.path.getmtime(filepath)
            # Calculate age in minutes
            age_seconds = now - mod_time
            age_in_minutes = age_seconds / 60

            if age_in_minutes > age_minutes:
                try:
                    os.remove(filepath)
                    print(f"Deleted old file: {filename}")
                except Exception as e:
                    print(f"Error deleting file {filename}: {e}")

if __name__ == '__main__':
    downloads_dir = os.path.join(os.getcwd(), 'downloads')
    # Run cleanup every 30 minutes (1800 seconds)
    while True:
        cleanup_downloads(downloads_dir, 30)
        time.sleep(1800)
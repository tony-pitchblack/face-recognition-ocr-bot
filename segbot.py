from newsurl_function import update_news_url
import subprocess

from pathlib import Path

CONFIGS_DIR = Path('./configs')

# update_news_url()

# Specify the audio stream (e.g., from a live stream or local file)
# news_url = "http://example.com/live_audio_stream"
with open(CONFIGS_DIR / 'news_url.txt', 'r') as f:
    news_url = f.read().strip()

# Define the duration (in seconds) for how long you want to capture the audio
duration_seconds = 30  # Capture for 30 seconds

# Output file name (e.g., "output.wav")
news_url = news_url.replace('&', r'\&')

# Build the ffmpeg command
ffmpeg_cmd = [
    "ffmpeg",
    "-y",                      # Overwrite output file if it exists
    "-i", news_url,            # Input URL
    "-loglevel", "debug",      # Enable detailed logging
    "-t", "30",                # Set duration to 30 seconds
    "-vn",                     # Exclude video stream
    "-acodec", "copy",         # Copy the audio codec without re-encoding
    "audio.mp4"                # Output file
]

# B# Start the ffmpeg process
ffmpeg_process = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE)

# Read audio data from the pipe
while True:
    audio_data = ffmpeg_process.stdout.read(1024)  # Read 1024 bytes of audio at a time
    if not audio_data:
        break  # Stop when no more audio data is available

    # Process the audio data (e.g., save to file or perform analysis)
    print(audio_data)  # Or replace with your audio processing code
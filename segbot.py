from newsurl_function import update_news_url
from urllib.parse import urlencode, quote
import subprocess

from pathlib import Path

HOST = '158.160.146.215'

# MODEL = "Systran/faster-whisper-medium"
# MODEL = "Systran/faster-whisper-base"
# MODEL = "Systran/faster-whisper-small"
MODEL = "Systran/faster-whisper-tiny"

# Define parameters as a dictionary
options = {
    # "file": f"@{audio_path_abs}",
    "language": "ru",
    "model": MODEL,
    "response_format": "verbose_json"
}

# Base URL
BASE_WS_URL = f"ws://{HOST}:8000/v1/audio/transcriptions"

# Construct the full URL with encoded query parameters
ws_url_with_options = f"{BASE_WS_URL}?{urlencode(options, quote_via=quote)}".replace('&', '\&')

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

def read_audio():
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

def read_resample_transcribe_audio():
    # Step 1: Run the first FFmpeg command to extract audio
    ffmpeg_cmd1 = [
        "ffmpeg", 
        "-i", news_url,
        "-loglevel", "debug",
        "-vn",  # No video
        "-acodec", "copy",  # Copy the audio codec
        "-f", "wav",  # Output format as WAV
        "pipe:1"  # Output to pipe
    ]

    # Step 2: Run the second FFmpeg command to process the audio
    ffmpeg_cmd2 = [
        "ffmpeg", 
        "-y",
        "-i", "pipe:0",  # Take input from the previous pipe
        "-ac", "1",  # Mono audio
        "-ar", "16000",  # Sample rate of 16 kHz
        "-f", "s16le",  # Output as signed 16-bit little-endian PCM
        "-acodec", "pcm_s16le", 
        "pipe:1"  # Output to pipe
    ]

    # Step 3: Use `pv` to throttle the data rate
    pv_cmd = ["pv", "-qL", "32000"]

    # Step 4: Send the data to websocat
    websocat_cmd = [
        "websocat", 
        "-v", 
        "--no-close", 
        "--binary", 
        ws_url_with_options
    ]

    # Chain the commands using subprocess.Popen
    try:
        ffmpeg_process1 = subprocess.Popen(ffmpeg_cmd1, stdout=subprocess.PIPE)
        ffmpeg_process2 = subprocess.Popen(ffmpeg_cmd2, stdin=ffmpeg_process1.stdout, stdout=subprocess.PIPE)
        pv_process = subprocess.Popen(pv_cmd, stdin=ffmpeg_process2.stdout, stdout=subprocess.PIPE)
        websocat_process = subprocess.Popen(websocat_cmd, stdin=pv_process.stdout)

        # Wait for processes to finish
        websocat_process.communicate()

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Cleanup all processes
        ffmpeg_process1.terminate()
        ffmpeg_process2.terminate()
        pv_process.terminate()
        websocat_process.terminate()

if __name__ == '__main__':
    # read_audio()
    read_resample_transcribe_audio()
import os
import json
import subprocess
import requests
import yt_dlp
from dotenv import load_dotenv

# Load API Key
load_dotenv()
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

if not DEEPGRAM_API_KEY:
    print("Deepgram API key not found in .env")
    exit()


# ---------------------------------------
# YOUTUBE METADATA EXTRACTION
# ---------------------------------------
def get_youtube_metadata(url):
    ydl_opts = {
        "quiet": True,
        "skip_download": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    metadata = {
        "title": info.get("title"),
        "creator": info.get("uploader"),
        "channel": info.get("channel"),
        "upload_date": info.get("upload_date"),
        "description": info.get("description"),
        "duration_seconds": info.get("duration"),
        "view_count": info.get("view_count"),
        "like_count": info.get("like_count"),
        "tags": info.get("tags")
    }

    return metadata


# ---------------------------------------
# DOWNLOAD AUDIO
# ---------------------------------------
def download_audio(url):
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "input.%(ext)s",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "quiet": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    print("Audio downloaded as input.mp3")


# ---------------------------------------
# TECHNICAL METADATA USING FFMPEG
# ---------------------------------------
def extract_audio_metadata(mp3_path):
    command = ["ffmpeg", "-i", mp3_path]

    result = subprocess.run(
        command,
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True
    )

    output = result.stderr
    metadata = {}

    for line in output.split("\n"):
        if "Duration" in line:
            metadata["duration"] = line.strip()
        if "bitrate" in line:
            metadata["bitrate"] = line.strip()
        if "Stream" in line and "Audio" in line:
            metadata["audio_stream_info"] = line.strip()

    metadata["file_size_mb"] = round(
        os.path.getsize(mp3_path) / (1024 * 1024), 2
    )

    return metadata


# ---------------------------------------
# SAVE METADATA.JSON
# ---------------------------------------
def save_metadata(youtube_meta, audio_meta):
    data = {
        "youtube_metadata": youtube_meta,
        "audio_metadata": audio_meta
    }

    with open("metadata.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print("metadata.json created")


# ---------------------------------------
# CONVERT TO MONO 16kHz WAV
# ---------------------------------------
def convert_to_mono(mp3_path):
    output_file = "processed_audio.wav"

    command = [
        "ffmpeg",
        "-y",
        "-i", mp3_path,
        "-ac", "1",
        "-ar", "16000",
        output_file
    ]

    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return output_file


# ---------------------------------------
# DEEPGRAM TRANSCRIPTION
# ---------------------------------------
def transcribe_with_deepgram(audio_path):
    url = "https://api.deepgram.com/v1/listen?model=nova-2&punctuate=true"

    headers = {
        "Authorization": f"Token {DEEPGRAM_API_KEY}",
        "Content-Type": "audio/wav"
    }

    with open(audio_path, "rb") as audio:
        response = requests.post(url, headers=headers, data=audio)

    if response.status_code != 200:
        print("Deepgram Error:", response.text)
        return None

    result = response.json()
    transcript = result["results"]["channels"][0]["alternatives"][0]["transcript"]

    return transcript


# ---------------------------------------
# SAVE TRANSCRIPTION.JSON
# ---------------------------------------
def save_transcription(text):
    data = {
        "transcription": text
    }

    with open("transcription.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print("transcription.json created")


# ---------------------------------------
# MAIN PIPELINE
# ---------------------------------------
def main():
    youtube_url = input("Enter YouTube URL: ")

    print("Extracting YouTube metadata...")
    youtube_metadata = get_youtube_metadata(youtube_url)

    print("Downloading audio...")
    download_audio(youtube_url)

    mp3_file = "input.mp3"

    if not os.path.exists(mp3_file):
        print("input.mp3 not found")
        return

    print("Extracting technical metadata...")
    audio_metadata = extract_audio_metadata(mp3_file)

    save_metadata(youtube_metadata, audio_metadata)

    print("Converting to mono...")
    processed_audio = convert_to_mono(mp3_file)

    print("Transcribing with Deepgram...")
    transcript = transcribe_with_deepgram(processed_audio)

    if transcript:
        save_transcription(transcript)
        print("Process completed successfully")
    else:
        print("Transcription failed")


if __name__ == "__main__":
    main()

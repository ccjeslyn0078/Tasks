import os
import json
import subprocess
import yt_dlp


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
# MAIN
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

    print("Metadata extraction completed successfully")


if __name__ == "__main__":
    main()

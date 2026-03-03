import os
import json
import subprocess
import requests
from dotenv import load_dotenv

# Load API key
load_dotenv()
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

if not DEEPGRAM_API_KEY:
    print("Deepgram API key not found in .env file")
    exit()


# -----------------------------------------
# Convert MP3 to WAV (Mono, 16kHz)
# -----------------------------------------
def convert_mp3_to_wav(mp3_path):
    output_wav = "processed_audio.wav"

    command = [
        "ffmpeg",
        "-y",
        "-i", mp3_path,
        "-ac", "1",          # mono
        "-ar", "16000",      # 16 kHz sample rate
        "-vn",
        output_wav
    ]

    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    if result.returncode != 0:
        print("FFmpeg conversion failed")
        return None

    return output_wav


# -----------------------------------------
# Send WAV to Deepgram
# -----------------------------------------
def transcribe_audio(wav_path):
    url = "https://api.deepgram.com/v1/listen?model=nova-2&punctuate=true"

    headers = {
        "Authorization": f"Token {DEEPGRAM_API_KEY}",
        "Content-Type": "audio/wav"
    }

    try:
        file_size = os.path.getsize(wav_path) / (1024 * 1024)
        print(f"WAV file size: {file_size:.2f} MB")
        print("Uploading audio to Deepgram...")

        with open(wav_path, "rb") as audio_file:
            response = requests.post(
                url,
                headers=headers,
                data=audio_file,
                timeout=(20, 600)   # 20 sec connect, 10 min read
            )

        if response.status_code != 200:
            print("Deepgram error:", response.text)
            return None

        result = response.json()
        transcript = result["results"]["channels"][0]["alternatives"][0]["transcript"]

        return transcript

    except requests.exceptions.RequestException as e:
        print("Network error:", e)
        return None


# -----------------------------------------
# Save transcription
# -----------------------------------------
def save_transcription(text):
    with open("transcription.json", "w", encoding="utf-8") as f:
        json.dump({"transcription": text}, f, indent=4)

    print("transcription.json created successfully")


# -----------------------------------------
# Main
# -----------------------------------------
def main():
    mp3_file = "input.mp3"

    if not os.path.exists(mp3_file):
        print("input.mp3 not found in project folder")
        return

    print("Converting MP3 to WAV...")
    wav_file = convert_mp3_to_wav(mp3_file)

    if not wav_file:
        return

    print("Starting transcription...")
    transcript = transcribe_audio(wav_file)

    if transcript:
        save_transcription(transcript)
        print("Transcription completed successfully")
    else:
        print("Transcription failed")


if __name__ == "__main__":
    main()

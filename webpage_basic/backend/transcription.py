import assemblyai as aai
import os

aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")

def transcribe_audio(file_path):

    config = aai.TranscriptionConfig(
        speaker_labels=True,
        speech_models=["universal-2"]
    )

    transcriber = aai.Transcriber()

    transcript = transcriber.transcribe(file_path, config)

    segments = []

    for utterance in transcript.utterances:

        segments.append({
            "speaker": f"Speaker {utterance.speaker}",
            "start": utterance.start / 1000,
            "end": utterance.end / 1000,
            "text": utterance.text
        })

    return segments

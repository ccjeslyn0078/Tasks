from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import shutil
import os

from mistral_ocr import extract_pdf
from transcription import transcribe_audio

app = FastAPI()

last_pdf_result = {}

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Serve frontend
app.mount("/static", StaticFiles(directory="../frontend"), name="static")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


@app.get("/")
def home():
    return FileResponse("../frontend/index.html")


@app.get("/result")
def result():
    return FileResponse("../frontend/result.html")


@app.post("/upload")
async def upload(file: UploadFile = File(...)):

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    if file.filename.endswith(".pdf"):

        text = extract_pdf(file_path)

        global last_pdf_result
        last_pdf_result = {
            "pdf_url": f"/uploads/{file.filename}",
            "content": text
        }

        return {
            "type": "pdf"
        }

    elif file.filename.endswith(".mp3"):

        transcript = transcribe_audio(file_path)

        return {
            "type": "mp3",
            "audio_url": f"/uploads/{file.filename}",
            "content": transcript
        }


@app.get("/upload_result")
def get_pdf_result():
    return last_pdf_result

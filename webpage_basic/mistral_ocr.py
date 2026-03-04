from mistralai import Mistral
import os

API_KEY = "cS6p8xSNfr9JHuLX7iUS7AovXyBiCqYZ"

client = Mistral(api_key=API_KEY)


def extract_pdf(file_path):

    uploaded = client.files.upload(
        file={
            "file_name": "document.pdf",
            "content": open(file_path, "rb")
        },
        purpose="ocr"
    )

    signed_url = client.files.get_signed_url(file_id=uploaded.id)

    response = client.ocr.process(
        model="mistral-ocr-latest",
        document={
            "type": "document_url",
            "document_url": signed_url.url
        }
    )

    text = ""

    for page in response.pages:
        text += page.markdown + "\n"

    return text

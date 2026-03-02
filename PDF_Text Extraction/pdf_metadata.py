import json
import os
from pypdf import PdfReader

def extract_pdf_metadata(pdf_path):
    if not pdf_path.endswith(".pdf"):
        raise ValueError("Only PDF files are valid.")

    reader = PdfReader(pdf_path)
    metadata = reader.metadata

    data = {
        "title": metadata.title,
        "author": metadata.author,
        "subject": metadata.subject,
        "keywords": metadata.get("/Keywords"),
        "creator": metadata.creator,
        "producer": metadata.producer,
        "creation_date": metadata.get("/CreationDate"),
        "modification_date": metadata.get("/ModDate"),
        "page_count": len(reader.pages)
    }

    return data


def save_json(data, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


if __name__ == "__main__":
    pdf_path = "sample.pdf"
    data = extract_pdf_metadata(pdf_path)
    print(data)

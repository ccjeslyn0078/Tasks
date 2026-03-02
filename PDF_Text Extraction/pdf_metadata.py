import json
from pypdf import PdfReader


def extract_title_from_text(text):
    lines = text.split("\n")

    for line in lines:
        line = line.strip()

        # Skip journal header lines
        if (
            len(line) > 10
            and "IJRAR" not in line
            and "Volume" not in line
            and "ISSN" not in line
        ):
            return line

    return "Unknown Title"


def extract_author_from_text(text):
    lines = text.split("\n")

    for line in lines:
        if "Dr." in line or "Professor" in line:
            return line.strip()

    return "Not Provided"


def extract_pdf_metadata(pdf_path):
    if not pdf_path.endswith(".pdf"):
        raise ValueError("Only PDF files are allowed.")

    reader = PdfReader(pdf_path)
    metadata = reader.metadata

    first_page_text = reader.pages[0].extract_text()

    # Title
    title = metadata.title if metadata.title else extract_title_from_text(first_page_text)

    # Author
    author = metadata.author if metadata.author else extract_author_from_text(first_page_text)

    data = {
        "title": title,
        "author": author,
        "subject": metadata.subject if metadata.subject else "Not Provided",
        "keywords": metadata.get("/Keywords") if metadata.get("/Keywords") else "Not Provided",
        "creator": metadata.creator,
        "producer": metadata.producer,
        "creation_date": metadata.get("/CreationDate"),
        "modification_date": metadata.get("/ModDate"),
        "page_count": len(reader.pages)
    }

    return data


def save_json(data, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    pdf_path = "sample.pdf"

    metadata_data = extract_pdf_metadata(pdf_path)
    save_json(metadata_data, "metadata_output.json")

    print("Metadata JSON file created successfully!")

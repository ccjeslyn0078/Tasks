from pypdf import PdfReader
import json

def extract_pdf_text(pdf_path):
    reader = PdfReader(pdf_path)
    pages_data = []

    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        page_info = {
            "page_number": i + 1,
            "content": text.strip() if text else ""
        }
        pages_data.append(page_info)

    return pages_data


if __name__ == "__main__":
    pdf_path = "sample.pdf"
    content = extract_pdf_text(pdf_path)

    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(content, f, indent=4, ensure_ascii=False)

    print("JSON file created successfully!")

from io import BytesIO

import pymupdf
from docx import Document
from werkzeug.datastructures import FileStorage


ALLOWED_EXTENSIONS = {"pdf", "docx"}


def extract_text(upload: FileStorage) -> str:
    extension = upload.filename.rsplit(".", 1)[-1].lower() if "." in upload.filename else ""
    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError("Please upload a PDF or DOCX resume.")

    raw_file = upload.read()
    if not raw_file:
        raise ValueError("The uploaded file is empty.")

    if extension == "pdf":
        document = pymupdf.open(stream=raw_file, filetype="pdf")
        text = "\n".join(page.get_text() for page in document)
    else:
        document = Document(BytesIO(raw_file))
        text = "\n".join(paragraph.text for paragraph in document.paragraphs)

    text = text.strip()
    if len(text) < 30:
        raise ValueError("No readable resume text was found in this file.")
    return text[:30000]

import os
from PyPDF2 import PdfReader

# Load upload directory from .env or use default
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "/data/uploads")

# Ensure directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)


def save_upload_file(file_bytes, filename):
    """
    Save an uploaded file (bytes) to the upload directory.
    """
    path = os.path.join(UPLOAD_DIR, filename)

    with open(path, "wb") as f:
        f.write(file_bytes)

    return path


def extract_text_from_pdf(path):
    """
    Extract text from a PDF file using PyPDF2.
    """
    try:
        reader = PdfReader(path)
        texts = []

        for page in reader.pages:
            texts.append(page.extract_text() or "")

        return "\n".join(texts)

    except Exception as e:
        return f"[error reading pdf] {e}"

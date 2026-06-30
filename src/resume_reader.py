from pathlib import Path

import fitz

from src.config import RESUME_DIR


SUPPORTED_EXTENSIONS = [".pdf"]


def find_resume() -> Path:
    if not RESUME_DIR.exists():
        raise FileNotFoundError("The 'resume' directory does not exist.")

    files = [
        file
        for file in RESUME_DIR.iterdir()
        if file.is_file() and file.suffix.lower() in SUPPORTED_EXTENSIONS
    ]

    if not files:
        raise FileNotFoundError(
            "No supported resume file found in the 'resume' directory."
        )

    if len(files) > 1:
        raise ValueError(
            "Multiple resume files found. Keep only one resume file in the 'resume' directory."
        )

    return files[0]


def read_pdf(path: Path) -> str:
    doc = fitz.open(path)
    text = "\n".join(page.get_text() for page in doc).strip()

    if not text:
        raise ValueError(
            "Failed to extract text from the PDF. The resume may be a scanned document."
        )

    return text


def load_resume() -> str:
    resume_path = find_resume()

    if resume_path.suffix.lower() == ".pdf":
        return read_pdf(resume_path)

    raise ValueError(f"Unsupported resume format: {resume_path.suffix}")
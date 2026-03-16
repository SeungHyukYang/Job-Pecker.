from pathlib import Path
from typing import List
import shutil
from fastapi import UploadFile

from core.docx_reader import read_docx_text

UPLOAD_ROOT = Path("data/uploads")
RESUME_DIR = UPLOAD_ROOT / "resumes"
COVER_LETTER_DIR = UPLOAD_ROOT / "cover_letters"

RESUME_DIR.mkdir(parents=True, exist_ok=True)
COVER_LETTER_DIR.mkdir(parents=True, exist_ok=True)


def has_uploaded_documents() -> bool:
    return any(RESUME_DIR.iterdir()) and any(COVER_LETTER_DIR.iterdir())


def save_uploaded_resumes(files: List[UploadFile]):
    for existing_file in RESUME_DIR.iterdir():
        if existing_file.is_file():
            existing_file.unlink()

    for file in files:
        if not file.filename:
            continue

        destination = RESUME_DIR / file.filename
        with destination.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)


def save_uploaded_cover_letter(file: UploadFile):
    for existing_file in COVER_LETTER_DIR.iterdir():
        if existing_file.is_file():
            existing_file.unlink()

    if not file.filename:
        return

    destination = COVER_LETTER_DIR / file.filename
    with destination.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)


def list_uploaded_resumes():
    return [file.name for file in RESUME_DIR.iterdir() if file.is_file()]


def get_uploaded_cover_letter_name():
    files = [file.name for file in COVER_LETTER_DIR.iterdir() if file.is_file()]
    return files[0] if files else None


def get_uploaded_resume_paths():
    return [file for file in RESUME_DIR.iterdir() if file.is_file()]


def get_uploaded_cover_letter_path():
    files = [file for file in COVER_LETTER_DIR.iterdir() if file.is_file()]
    return files[0] if files else None


def get_primary_resume_path():
    files = get_uploaded_resume_paths()
    return files[0] if files else None


def read_primary_resume_text() -> str:
    file_path = get_primary_resume_path()
    if not file_path:
        return ""
    return read_docx_text(file_path)


def read_uploaded_cover_letter_text() -> str:
    file_path = get_uploaded_cover_letter_path()
    if not file_path:
        return ""
    return read_docx_text(file_path)
from pathlib import Path
from docx import Document


def read_docx_text(file_path: str | Path) -> str:
    path = Path(file_path)

    if not path.exists():
        return ""

    if path.suffix.lower() != ".docx":
        return ""

    try:
        document = Document(path)
        lines = []

        for paragraph in document.paragraphs:
            text = paragraph.text.strip()
            if text:
                lines.append(text)

        return "\n".join(lines)
    except Exception:
        return ""
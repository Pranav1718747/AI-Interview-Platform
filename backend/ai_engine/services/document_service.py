import os
from .pdf_service import extract_text_from_pdf
from .docx_service import extract_text_from_docx


def extract_document_text(file_path: str) -> str:
    """
    Extracts text from a document based on its file extension.
    Supports PDF (.pdf), Word Documents (.docx), and plain text files (.txt).
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found at path: {file_path}")

    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".docx":
        return extract_text_from_docx(file_path)
    elif ext in [".txt", ".md"]:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    else:
        # Fallback to general read or PDF attempt
        try:
            return extract_text_from_pdf(file_path)
        except Exception:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()

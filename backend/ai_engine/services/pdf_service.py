import logging

logger = logging.getLogger(__name__)


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text from a PDF file using PyMuPDF (fitz) or pypdf.
    """
    # Try fitz (PyMuPDF) first
    try:
        import fitz
        doc = fitz.open(file_path)
        text = ""
        try:
            for page in doc:
                text += page.get_text() + "\n"
        finally:
            doc.close()
        if text.strip():
            return text
    except ImportError:
        pass
    except Exception as e:
        logger.warning(f"PyMuPDF failed: {e}, falling back to pypdf")

    # Fallback to pypdf
    try:
        from pypdf import PdfReader
        reader = PdfReader(file_path)
        text_pages = []
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text_pages.append(extracted)
        return "\n".join(text_pages)
    except Exception as e:
        logger.error(f"pypdf failed to extract text: {e}")
        raise ValueError(f"Could not extract text from PDF: {str(e)}")
from PyPDF2 import PdfReader

def extract_text(file_path: str) -> str:
    reader = PdfReader(file_path)
    return " ".join(page.extract_text() or "" for page in reader.pages)

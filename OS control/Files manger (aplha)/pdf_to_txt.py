import os
import pdfplumber
import pytesseract
from pdf2image import convert_from_path

# Tesseract path (important for Windows)
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\DHRUV\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"


def extract_text_from_pdf(path: str) -> str:
    # Extract text from normal (selectable text) PDFs
    text = ""

    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += " " + page_text

    return text


def ocr_from_pdf(path: str, poppler_path: str | None = None) -> str:
    # Extract text from scanned PDFs using OCR
    text = ""

    images = convert_from_path(
        path,
        dpi=200,
        poppler_path=poppler_path
    )

    for img in images:
        text += " " + pytesseract.image_to_string(img)

    return text


def smart_pdf_reader(path: str, poppler_path: str | None = None) -> str:
    # Try normal extraction first
    text = extract_text_from_pdf(path)

    # If no text found → run OCR
    if os.path.getsize(path) > 0 and not text.strip():
        text = ocr_from_pdf(path, poppler_path)

    return text
    
poppler_path = r"C:\Users\DHRUV\OneDrive\Desktop\LUNA\poppler-25.12.0\Library\bin"

if __name__ == "__main__" :
    # -------- TEST --------
    poppler_path = r"C:\Users\DHRUV\OneDrive\Desktop\LUNA\poppler-25.12.0\Library\bin"

    text = smart_pdf_reader("test.pdf", poppler_path)

    print(text)
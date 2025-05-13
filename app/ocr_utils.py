import pytesseract
from pdf2image import convert_from_path

def pdf_to_text(pdf_path):
    """Convert PDF to text using Tesseract OCR."""
    images = convert_from_path(pdf_path)
    text = ""
    for image in images:
        text += pytesseract.image_to_string(image)
    return text

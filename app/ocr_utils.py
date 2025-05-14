"""
import pytesseract
from pdf2image import convert_from_path

def pdf_to_text(pdf_path):
    Convert PDF to text using Tesseract OCR.
    images = convert_from_path(pdf_path)
    text = ""
    for image in images:
        text += pytesseract.image_to_string(image)
    return text
"""


import fitz  # PyMuPDF

def pdf_to_text(pdf_path):
    """Extract text from PDF using PyMuPDF."""
    doc = fitz.open(pdf_path)  # Open the PDF file
    text = ""
    for page in doc:
        text += page.get_text("text")  # Extract text from each page
    return text

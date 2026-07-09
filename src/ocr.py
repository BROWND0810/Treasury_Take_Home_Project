"""
OCR helper functions.
Uses Tesseract OCR through pytesseract.
"""

from PIL import Image
from pathlib import Path


def extract_text_from_image(image: Image.Image) -> str:
    """
    Extract visible text from a PIL image.
    """

    try:
        import pytesseract

        tesseract_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

        if not Path(tesseract_path).exists():
            return (
                "OCR failed.\n\n"
                "Tesseract error: Tesseract OCR was not found at "
                "C:\\Program Files\\Tesseract-OCR\\tesseract.exe."
            )

        pytesseract.pytesseract.tesseract_cmd = tesseract_path

        return pytesseract.image_to_string(image)

    except Exception as error:
        return (
            "OCR failed.\n\n"
            f"Tesseract error: {error}\n\n"
            "Confirm that pytesseract and Tesseract OCR are installed."
        )
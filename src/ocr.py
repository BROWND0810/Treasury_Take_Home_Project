"""
OCR helper functions.
Uses Tesseract OCR through pytesseract.
Supports both local Windows use and Linux deployment.
"""

from PIL import Image
from pathlib import Path
import shutil


def find_tesseract_path() -> str | None:
    """
    Find the Tesseract executable on Windows or Linux.
    """

    possible_paths = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        "/usr/bin/tesseract",
        "/usr/local/bin/tesseract",
    ]

    for path in possible_paths:
        if Path(path).exists():
            return path

    system_path = shutil.which("tesseract")
    if system_path:
        return system_path

    return None


def extract_text_from_image(image: Image.Image) -> str:
    """
    Extract visible text from a PIL image.
    """

    try:
        import pytesseract

        tesseract_path = find_tesseract_path()

        if not tesseract_path:
            return (
                "OCR failed.\n\n"
                "Tesseract error: Tesseract OCR was not found.\n\n"
                "Confirm that Tesseract OCR is installed locally or available in the deployment environment."
            )

        pytesseract.pytesseract.tesseract_cmd = tesseract_path

        return pytesseract.image_to_string(image)

    except Exception as error:
        return (
            "OCR failed.\n\n"
            f"Tesseract error: {error}\n\n"
            "Confirm that pytesseract and Tesseract OCR are installed."
        )

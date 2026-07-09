"""
Utility functions.
"""

import re


def clean_text(text: str) -> str:
    """
    Clean OCR text for easier display.
    """

    if not text:
        return ""

    text = text.replace("\r", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)

    return text.strip()

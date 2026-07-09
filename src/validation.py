"""
Validation functions for comparing expected application data
against OCR text extracted from alcohol labels.
"""

import re
from difflib import SequenceMatcher


def normalize_text(value: str) -> str:
    """
    Normalize text for comparison.
    """

    if value is None:
        return ""

    value = value.upper()
    value = value.replace("’", "'")
    value = re.sub(r"[^A-Z0-9.%/()' -]", " ", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def similarity_score(left: str, right: str) -> float:
    """
    Return a fuzzy similarity score between two text values.
    """

    left_norm = normalize_text(left)
    right_norm = normalize_text(right)

    if not left_norm or not right_norm:
        return 0.0

    return SequenceMatcher(None, left_norm, right_norm).ratio()


def value_found(expected_value: str, extracted_text: str) -> bool:
    """
    Check if expected value appears in OCR text after normalization.
    """

    expected_norm = normalize_text(expected_value)
    extracted_norm = normalize_text(extracted_text)

    return expected_norm in extracted_norm


def warning_heading_is_valid(extracted_text: str) -> bool:
    """
    The warning heading should appear as GOVERNMENT WARNING:
    This check is stricter than normal field matching.
    """

    return "GOVERNMENT WARNING:" in extracted_text.upper()


def validate_label_fields(expected_fields: dict, extracted_text: str) -> list:
    """
    Validate expected fields against extracted OCR text.

    Returns:
        List of dictionaries for display in a table.
    """

    results = []

    for field_name, expected_value in expected_fields.items():
        expected_value = expected_value.strip() if expected_value else ""

        if not expected_value:
            results.append({
                "Field": field_name,
                "Expected": "",
                "Status": "Missing",
                "Confidence": "0%",
                "Reviewer Note": "Expected value was not provided."
            })
            continue

        if field_name == "Government Warning":
            result = validate_government_warning(expected_value, extracted_text)
        else:
            result = validate_general_field(field_name, expected_value, extracted_text)

        results.append(result)

    return results


def validate_general_field(field_name: str, expected_value: str, extracted_text: str) -> dict:
    """
    Validate standard label fields using exact and fuzzy matching.
    """

    if value_found(expected_value, extracted_text):
        return {
            "Field": field_name,
            "Expected": expected_value,
            "Status": "Match",
            "Confidence": "100%",
            "Reviewer Note": "Expected value appears on the label."
        }

    best_score = best_partial_similarity(expected_value, extracted_text)
    confidence = round(best_score * 100)

    if best_score >= 0.82:
        status = "Possible Match"
        note = "Text appears similar. Reviewer judgment recommended."
    elif best_score >= 0.60:
        status = "Mismatch"
        note = "Some similar text was found, but it may not match the expected value."
    else:
        status = "Missing"
        note = "Expected value was not clearly found on the label."

    return {
        "Field": field_name,
        "Expected": expected_value,
        "Status": status,
        "Confidence": f"{confidence}%",
        "Reviewer Note": note
    }


def validate_government_warning(expected_warning: str, extracted_text: str) -> dict:
    """
    Validate government warning with stricter rules.
    """

    heading_valid = warning_heading_is_valid(extracted_text)

    expected_norm = normalize_text(expected_warning)
    extracted_norm = normalize_text(extracted_text)

    if expected_norm in extracted_norm and heading_valid:
        return {
            "Field": "Government Warning",
            "Expected": "Standard warning text",
            "Status": "Match",
            "Confidence": "100%",
            "Reviewer Note": "Government warning appears to match the expected text and heading."
        }

    score = best_partial_similarity(expected_warning, extracted_text)
    confidence = round(score * 100)

    if not heading_valid:
        return {
            "Field": "Government Warning",
            "Expected": "Standard warning text",
            "Status": "Mismatch",
            "Confidence": f"{confidence}%",
            "Reviewer Note": "Required heading GOVERNMENT WARNING: was not found in the expected uppercase format."
        }

    if score >= 0.88:
        return {
            "Field": "Government Warning",
            "Expected": "Standard warning text",
            "Status": "Possible Match",
            "Confidence": f"{confidence}%",
            "Reviewer Note": "Warning text is similar, but manual review is recommended because this field requires strict wording."
        }

    return {
        "Field": "Government Warning",
        "Expected": "Standard warning text",
        "Status": "Mismatch",
        "Confidence": f"{confidence}%",
        "Reviewer Note": "Government warning text was not found or does not appear to match the expected wording."
    }


def best_partial_similarity(expected_value: str, extracted_text: str) -> float:
    """
    Compare expected text against chunks of extracted OCR text.
    This helps when OCR output is long.
    """

    expected_norm = normalize_text(expected_value)
    extracted_norm = normalize_text(extracted_text)

    if not expected_norm or not extracted_norm:
        return 0.0

    words = extracted_norm.split()
    expected_word_count = max(1, len(expected_norm.split()))

    best_score = 0.0

    for start in range(0, len(words)):
        end = start + expected_word_count + 4
        chunk = " ".join(words[start:end])
        score = similarity_score(expected_norm, chunk)

        if score > best_score:
            best_score = score

    return best_score

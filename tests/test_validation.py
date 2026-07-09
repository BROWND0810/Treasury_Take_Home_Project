"""
Basic validation tests.
Run with:
python -m pytest
"""

from src.validation import validate_label_fields


def test_exact_brand_match():
    expected = {
        "Brand Name": "OLD TOM DISTILLERY",
        "Government Warning": "GOVERNMENT WARNING: TEST WARNING"
    }

    extracted = "OLD TOM DISTILLERY\nGOVERNMENT WARNING: TEST WARNING"

    results = validate_label_fields(expected, extracted)
    assert results[0]["Status"] == "Match"
    assert results[1]["Status"] == "Match"


def test_missing_brand():
    expected = {
        "Brand Name": "OLD TOM DISTILLERY"
    }

    extracted = "SOME OTHER DISTILLERY"

    results = validate_label_fields(expected, extracted)
    assert results[0]["Status"] in ["Missing", "Mismatch"]

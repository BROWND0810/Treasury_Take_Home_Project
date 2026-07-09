# Sample Labels

This folder contains mock JPG alcohol labels for testing the AI-Powered Alcohol Label Verification Prototype.

These labels are fictional and were created only for software testing.

## Contents

Total JPG test labels: 33

The labels cover three beverage categories:

- Distilled Spirits
- Malt Beverages
- Wine

## Test Coverage

The labels include these test cases:

- Fully compliant labels
- Good labels with all core fields
- Labels with different or wrong ABV values
- Labels with bad government warning wording
- Labels with missing Government Warning
- Labels with lowercase or changed Government Warning heading
- Labels with unclear or low-quality image quality

## How to Use These Files

1. Open the Streamlit app.
2. Use `manifest_expected_values.csv` to find the expected values for a test label.
3. Enter the expected values into the app sidebar.
4. Upload the matching JPG label.
5. Review the app output for Match, Possible Match, Mismatch, or Missing results.

## Important Testing Note

For wrong ABV labels, enter the `expected_alcohol_content` from the manifest into the app. The label image will show a different value. The app should flag that issue.

For missing or bad warning labels, keep the standard `warning_expected_in_app` text in the app. The label image should cause a warning mismatch or missing-field result.

For low-quality labels, OCR may produce imperfect text. That is expected and helps test how the prototype handles unclear images.

## Files

- `manifest_expected_values.csv`: one combined manifest for all labels
- JPG files: mock test labels for upload into the app

# AI-Powered Alcohol Label Verification Prototype

## Overview

This project is a take-home prototype for an AI-powered alcohol label verification application.

The app helps a compliance reviewer compare visible alcohol label text against expected application data. It uses OCR to extract text from uploaded label images and then applies rule-based and fuzzy matching checks to identify matches, possible matches, missing fields, and mismatches.

The prototype is designed as a reviewer support tool. It does not replace official TTB compliance review or make final legal approval decisions.

## Problem Context

Alcohol label review requires reviewers to check whether information shown on a label matches information submitted in an application. Many of these checks involve comparing fields such as brand name, class/type, alcohol content, net contents, and the required Government Health Warning Statement.

This prototype focuses on reducing repetitive manual checking while keeping the reviewer in control. The app gives clear field-level results and flags items that may need manual review.

## Core Features

- Upload one or more alcohol label images
- Extract visible text using OCR
- Compare extracted label text against expected application data
- Validate common alcohol label fields
- Use stricter checks for the Government Warning field
- Display results as Match, Possible Match, Mismatch, or Missing
- Show confidence scores and reviewer notes
- Provide a batch summary for uploaded labels
- Allow batch summary download as a CSV file
- Include sample test labels for distilled spirits, malt beverages, and wine

## Fields Checked

The current prototype checks these fields:

- Brand Name
- Class / Type
- Alcohol Content
- Net Contents
- Government Warning

## Beverage Categories Covered by Test Labels

The included mock sample labels cover:

- Distilled Spirits
- Malt Beverages
- Wine

## Technology Stack

- Python
- Streamlit
- Tesseract OCR
- pytesseract
- pandas
- Pillow
- difflib fuzzy matching
- pytest

## Project Structure

```text
alcohol_label_ocr_app/
│
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── src/
│   ├── __init__.py
│   ├── ocr.py
│   ├── validation.py
│   └── utils.py
│
├── sample_labels/
│   ├── README.md
│   ├── manifest_expected_values.csv
│   └── *.jpg
│
└── tests/
    └── test_validation.py
```

## Local Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd alcohol_label_ocr_app
```

### 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Python dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Install Tesseract OCR

This project uses `pytesseract`, which requires the Tesseract OCR engine to be installed on the computer.

For Windows, one option is:

```powershell
winget install UB-Mannheim.TesseractOCR
```

The expected Windows install path is:

```text
C:\Program Files\Tesseract-OCR\tesseract.exe
```

The app points directly to that path in `src/ocr.py`.

If Tesseract is installed somewhere else, update the `tesseract_path` value in `src/ocr.py`.

### 5. Run the app

```bash
python -m streamlit run app.py
```

The app should open in the browser at:

```text
http://localhost:8501
```

## How to Use the App

1. Start the Streamlit app.
2. Enter expected application data in the sidebar.
3. Upload one or more label images.
4. Review the extracted OCR text.
5. Review the field verification table.
6. Check the overall result.
7. Download the batch summary CSV if needed.

## Sample Label Testing

The `sample_labels` folder contains mock JPG labels and a combined manifest file.

Use:

```text
sample_labels/manifest_expected_values.csv
```

to find the expected values for each test label.

Recommended test cases include:

- Fully compliant label
- Wrong or different ABV
- Bad Government Warning wording
- Missing Government Warning
- Lowercase or changed Government Warning heading
- Low-quality or unclear image

For a known successful test, use:

```text
distilled_spirits_good_1.jpg
```

with these expected values:

```text
Brand Name: OLD TOM DISTILLERY
Class / Type: Kentucky Straight Bourbon Whiskey
Alcohol Content: 45% Alc./Vol. (90 Proof)
Net Contents: 750 mL
```

Expected result:

```text
Overall Result: No Issues Found
Matches: 5
Possible Matches: 0
Issues: 0
```

## Validation Logic

The app uses two main validation approaches.

### General Field Checks

For brand name, class/type, alcohol content, and net contents, the app uses normalized text comparison and fuzzy matching.

Results may be:

- Match
- Possible Match
- Mismatch
- Missing

This allows the prototype to handle small differences such as capitalization or spacing while still flagging likely issues.

### Government Warning Check

The Government Warning is checked more strictly because warning wording and heading format matter. The app looks for the required warning content and the uppercase heading:

```text
GOVERNMENT WARNING:
```

If the warning is missing, changed, or formatted differently, the app recommends manual review.

## Assumptions

- The prototype is standalone and does not connect to COLA or any production Treasury system.
- Uploaded files are processed during the session and are not intentionally stored by the app.
- The app is for prototype screening only.
- Final compliance decisions remain with authorized reviewers.
- Test labels are fictional and used only for software testing.
- OCR performance depends on image quality, font size, lighting, glare, rotation, and resolution.
- The prototype focuses on common label fields, not every beverage-specific regulatory requirement.

## Known Limitations

- The app does not perform a complete legal compliance review.
- It does not validate every TTB rule for distilled spirits, malt beverages, or wine.
- OCR may struggle with curved bottles, glare, low resolution, small warning text, or poor lighting.
- The app does not include user authentication.
- The app does not integrate with COLA.
- The app does not permanently store review history.
- The app currently expects Tesseract OCR to be available locally or configured in the deployment environment.

## Testing

Run the included tests with:

```bash
python -m pytest
```

The current tests focus on validation logic.

## Deployment Notes

This app can be deployed to a public hosting service that supports Streamlit, such as Streamlit Community Cloud or another Python web app host.

Deployment must include:

- `app.py`
- `requirements.txt`
- `src/`
- `sample_labels/`
- `tests/`
- `README.md`

For deployment environments, Tesseract OCR must also be available. If the hosting platform does not support system-level Tesseract installation, the OCR setup may need to be adjusted.

## Design Decisions

The prototype favors:

- A simple reviewer-facing interface
- Fast field-level feedback
- Clear manual review flags
- Practical OCR extraction
- Transparent validation rules
- Batch upload support
- Clean code organization

The design intentionally avoids direct system integration, persistent storage, and complex authentication because the assignment requested a standalone proof of concept.

## Build Status

The prototype has been tested locally with mock label images.

Confirmed working:

- Streamlit app launch
- Image upload
- OCR text extraction with Tesseract
- Field comparison
- Government warning validation
- Batch summary output
- CSV download option
- Full-pass compliant label test

Known successful local test:

```text
distilled_spirits_good_1.jpg
Overall Result: No Issues Found
Matches: 5
Possible Matches: 0
Issues: 0
```

## Author

David A. Brown

## Disclaimer

This prototype is for demonstration and evaluation purposes only. It is not an official Treasury or TTB system and does not provide final regulatory approval.

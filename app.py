"""
Program: AI-Powered Alcohol Label Verification App
Author: David A. Brown
Date: July 2026
Purpose: Prototype app to extract text from alcohol labels and compare key label fields
against expected application data.
"""

import streamlit as st
import pandas as pd
from PIL import Image

from src.ocr import extract_text_from_image
from src.validation import validate_label_fields
from src.utils import clean_text

st.set_page_config(
    page_title="Alcohol Label Verification",
    page_icon="🏷️",
    layout="wide"
)

st.title("AI-Powered Alcohol Label Verification Prototype")

st.write(
    "Upload one or more alcohol label images. Enter the expected application data. "
    "The app extracts visible text from the label and checks for matches, possible matches, "
    "missing fields, or mismatches."
)

st.info(
    "Prototype note: This tool supports reviewer screening only. "
    "Final compliance decisions remain with authorized TTB reviewers."
)

with st.sidebar:
    st.header("Expected Application Data")

    brand_name = st.text_input("Brand Name", value="OLD TOM DISTILLERY")
    class_type = st.text_input("Class / Type", value="Kentucky Straight Bourbon Whiskey")
    alcohol_content = st.text_input("Alcohol Content", value="45% Alc./Vol. (90 Proof)")
    net_contents = st.text_input("Net Contents", value="750 mL")

    st.markdown("### Government Warning")
    government_warning = st.text_area(
        "Expected Warning Text",
        value=(
            "GOVERNMENT WARNING: (1) According to the Surgeon General, women should not drink "
            "alcoholic beverages during pregnancy because of the risk of birth defects. "
            "(2) Consumption of alcoholic beverages impairs your ability to drive a car or "
            "operate machinery, and may cause health problems."
        ),
        height=160
    )

uploaded_files = st.file_uploader(
    "Upload label image(s)",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True
)

expected_fields = {
    "Brand Name": brand_name,
    "Class / Type": class_type,
    "Alcohol Content": alcohol_content,
    "Net Contents": net_contents,
    "Government Warning": government_warning
}

if uploaded_files:
    batch_rows = []

    for uploaded_file in uploaded_files:
        st.divider()
        st.subheader(f"Review Results: {uploaded_file.name}")

        image = Image.open(uploaded_file).convert("RGB")

        left_col, right_col = st.columns([1, 2])

        with left_col:
            st.image(image, caption="Uploaded Label", use_container_width=True)

        with right_col:
            with st.spinner("Extracting text from label..."):
                extracted_text = extract_text_from_image(image)

            cleaned_text = clean_text(extracted_text)

            st.markdown("### Extracted OCR Text")
            st.text_area(
                label="OCR Output",
                value=cleaned_text,
                height=220,
                key=f"ocr_{uploaded_file.name}"
            )

            results = validate_label_fields(expected_fields, cleaned_text)

            st.markdown("### Field Verification")
            result_df = pd.DataFrame(results)
            st.dataframe(result_df, use_container_width=True, hide_index=True)

            pass_count = sum(1 for r in results if r["Status"] == "Match")
            warning_count = sum(1 for r in results if r["Status"] == "Possible Match")
            fail_count = sum(1 for r in results if r["Status"] in ["Mismatch", "Missing"])

            if fail_count > 0:
                overall = "Manual Review Required"
                st.error("Overall Result: Manual Review Required")
            elif warning_count > 0:
                overall = "Review Recommended"
                st.warning("Overall Result: Review Recommended")
            else:
                overall = "No Issues Found"
                st.success("Overall Result: No Issues Found")

            batch_rows.append({
                "File": uploaded_file.name,
                "Overall Result": overall,
                "Matches": pass_count,
                "Possible Matches": warning_count,
                "Issues": fail_count
            })

    st.divider()
    st.subheader("Batch Summary")

    batch_df = pd.DataFrame(batch_rows)
    st.dataframe(batch_df, use_container_width=True, hide_index=True)

    csv_data = batch_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Batch Summary CSV",
        data=csv_data,
        file_name="label_verification_summary.csv",
        mime="text/csv"
    )

else:
    st.write("Upload one or more label images to begin.")

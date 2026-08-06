"""Validator Agent Node."""

import pandas as pd
from src.state import SwarmState
from src.utils.validator import generate_cleaning_diff, format_validation_report


def data_validator(state: SwarmState) -> dict:
    """Loads raw and cleaned CSVs from disk and computes validation metrics."""
    print("\n🔍 [Node 4: Validator] Computing pre and post cleaning metrics from disk...")

    raw_path = state["input_file_path"]
    cleaned_path = state["output_file_path"]

    if not cleaned_path:
        print("❌ Validation skipped: No cleaned file path found in state.")
        return {"status": "failed"}

    # Load both files from disk for comparison
    df_raw = pd.read_csv(raw_path)
    df_cleaned = pd.read_csv(cleaned_path)

    diff_metrics = generate_cleaning_diff(df_raw, df_cleaned)
    report_text = format_validation_report(diff_metrics)

    print(report_text)

    return {
        "validation_report": diff_metrics,
        "status": "success",
    }
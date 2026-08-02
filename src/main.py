import io
import sys
from pathlib import Path
import pandas as pd

from src.config import DEFAULT_RAW_CSV, VALUE_COUNTS_TOP_N
from src.graph import build_graph
from src.state import SwarmState
from src.utils.generate_data import generate_messy_dataset


def prepare_data_preview(df: pd.DataFrame) -> str:
    """Generates a rich, dataset-agnostic structural summary across the ENTIRE dataset."""
    # 1. Capture df.info() (Column types and non-null counts across ALL rows)
    buffer = io.StringIO()
    df.info(buf=buffer)
    info_str = buffer.getvalue()

    # 2. Extract top value distributions for text/categorical columns to spot mixed noise/formatting
    unique_samples = {}
    for col in df.select_dtypes(include=["object", "string"]).columns:
        top_vals = df[col].dropna().value_counts().head(VALUE_COUNTS_TOP_N).index.tolist()
        unique_samples[col] = top_vals

    # 3. Numerical describe() summary to spot outlier sentinels (e.g., -99, -999)
    num_describe = df.describe().to_string() if not df.select_dtypes(include=["number"]).empty else "No numeric columns."

    summary = f"""=== 1. DATASET OVERVIEW ({len(df)} Total Rows) ===
{info_str}

=== 2. NUMERICAL SUMMARY (Check min/max for sentinel values like -99) ===
{num_describe}

=== 3. CATEGORICAL & STRING SAMPLES (Check top value formats/currency noise) ===
{unique_samples}

=== 4. FIRST 5 ROWS ===
{df.head().to_string()}
"""
    return summary


def main():
    target_csv = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_RAW_CSV

    # Auto-generate messy dummy file if default path doesn't exist yet
    if not target_csv.exists() and target_csv == DEFAULT_RAW_CSV:
        print("ℹ️ No target CSV found. Generating messy dummy dataset...")
        generate_messy_dataset(str(target_csv))

    if not target_csv.exists():
        print(f"❌ Error: Target file '{target_csv}' does not exist.")
        sys.exit(1)

    print(f"📂 Loading dataset: '{target_csv}'...")
    raw_df = pd.read_csv(target_csv)

    print("📊 Profiling dataset structure...")
    data_summary = prepare_data_preview(raw_df)

    initial_state: SwarmState = {
        "file_path": str(target_csv),
        "data_preview": data_summary,
        "issues_found": "",
        "generated_code": "",
        "error_log": [],
        "retry_count": 0,
        "status": "processing",
    }

    print("🤖 Initializing Tidy Swarm Pipeline...")
    app = build_graph()
    final_state = app.invoke(initial_state)

    print("\n-------------------------------------------")
    print(f"🏁 Execution Finished: STATUS = {final_state['status'].upper()}")
    print("-------------------------------------------")


if __name__ == "__main__":
    main()
"""Data Validation and Metrics Diff Engine."""

from typing import Any, Dict
import pandas as pd


def generate_cleaning_diff(df_before: pd.DataFrame, df_after: pd.DataFrame) -> Dict[str, Any]:
    """Computes a structured diff comparing raw and cleaned DataFrames."""
    # 1. Row & Column Count Deltas
    rows_before, cols_before = df_before.shape
    rows_after, cols_after = df_after.shape

    # 2. Memory Footprint Delta (in KB)
    mem_before_kb = round(df_before.memory_usage(deep=True).sum() / 1024, 2)
    mem_after_kb = round(df_after.memory_usage(deep=True).sum() / 1024, 2)
    mem_reduction_pct = (
        round(((mem_before_kb - mem_after_kb) / mem_before_kb) * 100, 2)
        if mem_before_kb > 0
        else 0.0
    )

    # 3. Column-level Nulls and Data Type Migrations
    col_metrics = []
    all_columns = sorted(list(set(df_before.columns).union(set(df_after.columns))))

    for col in all_columns:
        in_before = col in df_before.columns
        in_after = col in df_after.columns

        dtype_before = str(df_before[col].dtype) if in_before else "DROPPED"
        dtype_after = str(df_after[col].dtype) if in_after else "DROPPED"

        nulls_before = int(df_before[col].isna().sum()) if in_before else 0
        nulls_after = int(df_after[col].isna().sum()) if in_after else 0
        nulls_fixed = nulls_before - nulls_after

        col_metrics.append(
            {
                "column": col,
                "dtype_before": dtype_before,
                "dtype_after": dtype_after,
                "nulls_before": nulls_before,
                "nulls_after": nulls_after,
                "nulls_fixed": nulls_fixed,
                "type_changed": dtype_before != dtype_after,
            }
        )

    total_nulls_before = sum(m["nulls_before"] for m in col_metrics)
    total_nulls_after = sum(m["nulls_after"] for m in col_metrics)

    return {
        "rows_before": rows_before,
        "rows_after": rows_after,
        "rows_dropped": rows_before - rows_after,
        "cols_before": cols_before,
        "cols_after": cols_after,
        "mem_before_kb": mem_before_kb,
        "mem_after_kb": mem_after_kb,
        "mem_reduction_pct": mem_reduction_pct,
        "total_nulls_before": total_nulls_before,
        "total_nulls_after": total_nulls_after,
        "total_nulls_fixed": total_nulls_before - total_nulls_after,
        "column_metrics": col_metrics,
    }


def format_validation_report(diff: Dict[str, Any]) -> str:
    """Formats the diff metrics dictionary into a clean CLI report string."""
    report = []
    report.append("=======================================================")
    report.append("📊 TIDY SWARM VALIDATION & METRICS REPORT")
    report.append("=======================================================")

    report.append("\n📈 SUMMARY METRICS:")
    report.append(f"  • Row Count:       {diff['rows_before']} ➔ {diff['rows_after']} ({diff['rows_dropped']} rows removed)")
    report.append(f"  • Column Count:    {diff['cols_before']} ➔ {diff['cols_after']}")
    report.append(f"  • Memory Usage:    {diff['mem_before_kb']} KB ➔ {diff['mem_after_kb']} KB ({diff['mem_reduction_pct']}% reduction)")
    report.append(f"  • Missing Values:  {diff['total_nulls_before']} ➔ {diff['total_nulls_after']} ({diff['total_nulls_fixed']} nulls resolved)")

    report.append("\n🔍 COLUMN-LEVEL TRANSFORMATION MATRIX:")
    report.append(f"{'Column Name':<20} | {'Dtype Shift':<22} | {'Nulls (Before ➔ After)':<22} | {'Status'}")
    report.append("-" * 80)

    for col in diff["column_metrics"]:
        c_name = col["column"][:18]
        type_shift = f"{col['dtype_before']} ➔ {col['dtype_after']}"
        null_shift = f"{col['nulls_before']} ➔ {col['nulls_after']}"

        status_flags = []
        if col["type_changed"]:
            status_flags.append("Type Casted")
        if col["nulls_fixed"] > 0:
            status_flags.append(f"Fixed {col['nulls_fixed']} Nulls")
        if col["dtype_after"] == "DROPPED":
            status_flags.append("Column Dropped")

        status_str = ", ".join(status_flags) if status_flags else "Unchanged"

        report.append(f"{c_name:<20} | {type_shift:<22} | {null_shift:<22} | {status_str}")

    report.append("=======================================================")
    return "\n".join(report)
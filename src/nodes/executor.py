import re
import pandas as pd
from src.state import SwarmState
from src.config import DEFAULT_CLEANED_CSV

def code_executor(state: SwarmState) -> dict:
    """
    The Executor agent runs the generated Pandas code to clean the dataset.
    It updates the state with the cleaned dataset and any error logs if execution fails.
    """
    print("\n🚀 [Node 3: Executor] Running code directly on memory DataFrame...")
    code_raw = state.get("generated_code", "")

    # Extract code from markdown fences (handles ```python ... ``` or generic ``` ... ```)
    match = re.search(r"```python\n(.*?)```", code_raw, re.DOTALL)
    if not match:
        match = re.search(r"```\n(.*?)```", code_raw, re.DOTALL)

    if not match:
        print("❌ Failed to parse Python code block.")
        return {
            "error_log": "SyntaxError: No markdown code block (```python ... ```) found in response.",
            "status": "failed",
        }

    pure_code = match.group(1).strip()

    # Initialize an empty error log
    error_log = None

    try:
        # Create a deep copy of the DataFrame for safe execution
        working_df = state["df"].copy()

        # Prepare an isolated local execution scope
        local_vars = {"df": working_df, "pd": pd}

        # Execute generated Pandas code
        exec(pure_code, {}, local_vars)

        cleaned_df = local_vars.get("df")
        if cleaned_df is None or not isinstance(cleaned_df, pd.DataFrame):
            raise ValueError("Execution finished, but 'df' was removed or lost.")

        # Determine output path and save cleaned output CSV
        input_path = state.get("file_path", str(DEFAULT_CLEANED_CSV))
        output_file = input_path.replace(".csv", "_cleaned.csv")
        cleaned_df.to_csv(output_file, index=False)

        print(
            f"🎉 Cleaning Succeeded! Clean DataFrame updated in state ({len(cleaned_df)} rows)."
        )
        print(f"💾 Output saved to: '{output_file}'")

        return {
            "df": cleaned_df,  # Update the DataFrame object directly in state!
            "status": "success",
            "error_log": None,
        }

    except Exception as e:
        # Capture any errors during execution
        error_log = str(e)

        # Update the state with failure status and error log
        return {
            "status": "failed",
            "error_log": error_log
        }
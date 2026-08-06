import re
import pandas as pd
from src.state import SwarmState

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
            "error_log": ["SyntaxError: No markdown code block (```python ... ```) found."],
            "status": "failed",
        }

    pure_code = match.group(1).strip()
    input_file = state["input_file_path"]
    output_file = state["output_file_path"]

    try:
        # Create a deep copy of the DataFrame for safe execution
        working_df = pd.read_csv(input_file)

        # Prepare an isolated local execution scope
        local_vars = {"df": working_df, "pd": pd}

        # Execute generated Pandas code
        exec(pure_code, {}, local_vars)

        cleaned_df = local_vars.get("df")
        if cleaned_df is None or not isinstance(cleaned_df, pd.DataFrame):
            raise ValueError("Execution finished, but 'df' was removed or lost.")

        # Determine output path and save cleaned output CSV
        cleaned_df.to_csv(output_file, index=False)

        print(f"🎉 Cleaning Succeeded!")
        print(f"💾 Output saved to: '{output_file}'")

        return {
            "status": "success",
            "error_log": [],
        }

    except Exception as e:
        # Capture any errors during execution
        err_msg = f"Attempt {state.get('retry_count', 1)} Failed: {type(e).__name__}: {str(e)}"
        print(f"⚠️ Execution Error Caught: {err_msg}")

        # Update the state with failure status and error log
        return {
            "status": "failed",
            "error_log": [err_msg]
        }
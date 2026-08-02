from langchain_ollama import OllamaLLM
from src.state import SwarmState
from src.config import AUDITOR_MODEL, TEMPARATURE

def data_auditor(state: SwarmState) -> dict:
    """
    The Auditor agent inspects the dataset and identifies issues.
    It updates the state with an audit log of findings.
    """
    print(f"🔍 [Node 1: Auditor Agent ({AUDITOR_MODEL})] Inspecting data...")

    current_retry = state.get("retry_count", 0)

    # Initialize the Ollama model for auditing
    auditor_llm = OllamaLLM(model=AUDITOR_MODEL, temperature=TEMPARATURE)

    error_context = ""
    error_list = state.get("error_log", [])
    if error_list:
        formatted_history = "\n".join([f"  {idx + 1}. {err}" for idx, err in enumerate(error_list)])
        error_context = (
            f"\n\n🚨 PREVIOUS CODE EXECUTION FAILURE HISTORY ({len(error_list)} attempt(s)):\n"
            f"{formatted_history}\n\n"
            "CRITICAL INSTRUCTION: Analyze ALL past execution failures above. Ensure your new cleaning instructions "
            "do NOT re-introduce any bugs that caused earlier attempts to crash."
        )

    prompt = f"""You are a Principal Data Engineer and Auditor. Analyze the statistical profile of an UNKNOWN raw dataset below:

    DATASET PROFILE SUMMARY:
    {state['data_preview']}
    {error_context}

    YOUR TASK:
    Identify ALL data quality defects present across the columns in this dataset and output a prioritized, bulleted cleaning plan.

    Look for:
    1. **Numeric Columns:** String noise (currency symbols, units, commas), incorrect string data types, or sentinel missing values (e.g., -99, -999, 'N/A').
    2. **Date/Time Columns:** Inconsistent date/time string formats or unparsed timestamps.
    3. **Categorical/Text Columns:** Inconsistent casing, leading/trailing whitespace, or redundant values.
    4. **Structural Issues:** Duplicate rows, completely empty columns, or severe null values.

    INSTRUCTIONS:
    - Refer to columns EXACTLY by their real names as shown in the profile.
    - Only request fixes for issues that ACTUALLY exist in this dataset summary.
    - Output ONLY the bulleted tasks. Do NOT write Python code.
    """

    # Generate the audit log using the LLM
    audit_log = auditor_llm.invoke(prompt)
    print(f"✅ Audit completed")

    return {
        "issues_found": audit_log,
        "retry_count": current_retry + 1,
        "status": "processing",
    }
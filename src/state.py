import operator
import pandas as pd
from typing import TypedDict, Annotated, Dict, Any, Optional

class SwarmState(TypedDict):
    """Represents the shared memory state passed across agents."""
    input_file_path: str           # Path to the raw dataset
    output_file_path: str         # Path to the cleaned dataset
    data_preview: str
    issues_found: str        # Audit log written by Auditor
    generated_code: str      # Pandas cleaning code produced by Engineer
    error_log: Annotated[list[str], operator.add] # Error log from Executor if code fails
    retry_count: int         # Count to prevent infinite repair loops
    status: str              # Pipeline state: "processing", "success", or "failed"
    validation_report: Optional[Dict[str, Any]]
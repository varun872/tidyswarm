import pandas as pd
from typing import TypedDict, Optional

class SwarmState(TypedDict):
    """Represents the shared memory state passed across agents."""
    file_path: str           # Path to the raw dataset
    df: pd.DataFrame         # Pandas DataFrame containing the dataset
    data_preview: str
    issues_found: str        # Audit log written by Auditor
    generated_code: str      # Pandas cleaning code produced by Engineer
    error_log: Optional[str] # Error log from Executor if code fails
    retry_count: int         # Count to prevent infinite repair loops
    status: str              # Pipeline state: "processing", "success", or "failed"
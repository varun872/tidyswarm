from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

# Default File Locations
RAW_CSV = DATA_DIR / "raw_messy_data.csv"
CLEANED_CSV = DATA_DIR / "raw_messy_data_cleaned.csv"

# Ensure data directory exists on import
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Ollama Settings
AUDITOR_MODEL = "qwen2.5:7b"
ENGINEER_MODEL = "qwen2.5:7b"
TEMPARATURE = 0.0

# Graph Settings
MAX_RETRIES = 3

# Number of top unique values to display
VALUE_COUNTS_TOP_N = 5

# AST Security Whitelists
ALLOWED_MODULES = {"pandas", "numpy", "re", "datetime", "math", "string"}
FORBIDDEN_BUILTINS = {"eval", "exec", "open", "compile", "__import__", "globals", "locals", "getattr", "setattr", "delattr", "input", "exit", "quit"}
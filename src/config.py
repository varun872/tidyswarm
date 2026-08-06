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

# 
VALUE_COUNTS_TOP_N = 5  # Number of top unique values to display for categorical columns
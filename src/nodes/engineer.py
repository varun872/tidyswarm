from langchain_ollama import OllamaLLM
from src.state import SwarmState
from src.config import ENGINEER_MODEL, TEMPARATURE

def code_engineer(state: SwarmState) -> dict:
    """
    The Engineer agent generates Pandas code to clean the dataset based on the audit log.
    It updates the state with the generated cleaning code.
    """
    print(f"⚙️ [Node 2: Engineer Agent ({ENGINEER_MODEL})] Generating Pandas code...")

    # Initialize the Ollama model for engineering
    engineer_llm = OllamaLLM(model=ENGINEER_MODEL, temperature=TEMPARATURE)

    prompt = f"""You are a Senior Data Engineer. Write robust Pandas code to clean a DataFrame named `df`.

    CLEANING REQUIREMENTS:
    {state['issues_found']}

    CRITICAL CODE RULES & GUARDRAILS:
    1. Assume `df` is already loaded into memory. Do NOT read files or re-instantiate `df`.
    2. **Defensive Regex:** When cleaning numeric/currency columns, strip unwanted string characters safely.
    3. **Safe Parsing:** Use `pd.to_datetime(..., errors='coerce', format='mixed')` for dates and `pd.to_numeric(..., errors='coerce')` for numbers.
    4. **String Hygiene:** Safely handle string operations by ensuring the column is string type before applying `.str` methods.
    5. Fill missing values based on the column type: use median for numeric columns, mode for categorical columns, and a placeholder like 'Unknown' for text columns.
    6. Wrap your code inside a single standard markdown code block: ```python ... ```
    7. Return ONLY valid, runnable Python code inside the block—no intro text or conversational commentary.
    """

    response = engineer_llm.invoke(prompt)
    print(f"💻 Code Block Generated")

    return {
        "generated_code": response,
        "status": "processing"
    }
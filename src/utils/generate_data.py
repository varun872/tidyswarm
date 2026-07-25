import os
import random
import numpy as np
import pandas as pd

def generate_messy_dataset(file_path: str = "data/raw_messy_data.csv", num_rows: int = 100) -> str:
    """Generates a messy dataset for local testing."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    np.random.seed(42)
    random.seed(42)

    # 1. Messy Dates
    dates = []
    for _ in range(num_rows):
        r = random.random()
        if r < 0.1:
            dates.append(np.nan)
        elif r < 0.4:
            dates.append("2024-01-15")
        elif r < 0.7:
            dates.append("15/01/2024")
        else:
            dates.append("Jan 15, 2024")

    # 2. Dirty Revenue Values
    revenue = []
    for _ in range(num_rows):
        r = random.random()
        val = round(random.uniform(500.0, 15000.0), 2)
        if r < 0.15:
            revenue.append(np.nan)
        elif r < 0.4:
            revenue.append(f"${val:,.2f}")
        elif r < 0.7:
            revenue.append(f"INR {val:.0f}")
        elif r < 0.85:
            revenue.append(f"{val} USD")
        else:
            revenue.append(val)

    # 3. Categorical Values
    departments = [" Sales ", "sales", "ENGINEERING", "Engineering ", " Marketing", "marketing", np.nan]
    dept_column = [random.choice(departments) for _ in range(num_rows)]

    # 4. Outliers/Sentinel Values
    ages = []
    for _ in range(num_rows):
        r = random.random()
        if r < 0.1:
            ages.append(np.nan)
        elif r < 0.9:
            ages.append(random.randint(22, 60))
        else:
            ages.append(-99)

    df = pd.DataFrame({
        "Transaction_Date": dates,
        "Department": dept_column,
        "Revenue": revenue,
        "Employee_Age": ages,
        "Is_Active": [random.choice([True, False, "TRUE", "false", np.nan]) for _ in range(num_rows)]
    })

    # Add duplicate rows
    duplicate_rows = df.iloc[:5].copy()
    df = pd.concat([df, duplicate_rows], ignore_index=True)

    df.to_csv(file_path, index=False)
    print(f"✅ Generated messy dataset at '{file_path}' ({len(df)} rows).")
    return file_path

if __name__ == "__main__":
    generate_messy_dataset()
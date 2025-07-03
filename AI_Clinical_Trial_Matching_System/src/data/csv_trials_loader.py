# src/data/csv_trials_loader.py
import pandas as pd

def load_trials_from_csv(csv_path: str):
    """
    Loads clinical trials from a CSV file.
    Expects columns: nct_id, title, inclusion, exclusion
    """
    df = pd.read_csv(csv_path)
    required_columns = {"nct_id", "title", "inclusion", "exclusion"}
    if not required_columns.issubset(set(df.columns)):
        raise ValueError(f"CSV is missing required columns: {required_columns - set(df.columns)}")

    trials = df.to_dict(orient="records")
    print(f"Loaded {len(trials)} clinical trials from {csv_path}")
    return trials

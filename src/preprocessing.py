import pandas as pd
import os

def load_raw_data(file_path):
    """Load raw dataset safely."""
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        raise FileNotFoundError(f"Dataset not found at {file_path}")
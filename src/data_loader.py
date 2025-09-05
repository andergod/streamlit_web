import pandas as pd

def load_data(path: str) -> pd.DataFrame:
    """Load dataset from CSV"""
    return pd.read_csv(path)

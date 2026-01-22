import pandas as pd

def sanitize_value(value):
    if value is None:
        return None
    if pd.isna(value):
        return None
    return value

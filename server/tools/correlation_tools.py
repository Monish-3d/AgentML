import pandas as pd

def correlation_matrix(df: pd.DataFrame):
    numeric = df.select_dtypes(include=["int64", "float64"])
    if numeric.shape[1] > 1:
        return numeric.corr().round(4)
    return None

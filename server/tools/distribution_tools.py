import pandas as pd

def compute_skewness(df: pd.DataFrame) -> dict:
    skewness = {}
    numeric = df.select_dtypes(include=["int64", "float64"])
    for col in numeric.columns:
        skewness[col] = round(float(df[col].skew()), 4)
    return skewness

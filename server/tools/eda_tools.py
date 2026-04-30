import pandas as pd


def dataset_summary(df: pd.DataFrame) -> dict:
    return {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "column_names": list(df.columns),
        "dtypes": df.dtypes.astype(str).to_dict(),
    }

def missing_values(df: pd.DataFrame) -> dict:
    # Returns a plain dict - JSON-safe
    return df.isnull().sum().to_dict()


def statistics(df: pd.DataFrame) -> dict:
    # Returns a nested dict - JSON-safe
    return df.describe(include="all").fillna("").to_dict()

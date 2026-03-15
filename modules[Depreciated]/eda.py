import pandas as pd

def dataset_summary(df):

    summary = {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "column_names": list(df.columns)
    }

    return summary


def missing_values(df):

    return df.isnull().sum()


def statistics(df):

    return df.describe()


def correlation_matrix(df):

    numeric_df = df.select_dtypes(include=["int64", "float64"])

    if numeric_df.shape[1] > 1:
        return numeric_df.corr()

    return None
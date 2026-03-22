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
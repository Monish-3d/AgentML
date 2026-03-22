def correlation_matrix(df):

    numeric = df.select_dtypes(include=["int64", "float64"])

    if numeric.shape[1] > 1:
        return numeric.corr()

    return None
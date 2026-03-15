def compute_skewness(df):

    skewness = {}

    numeric = df.select_dtypes(include=["int64", "float64"])

    for col in numeric.columns:
        skewness[col] = df[col].skew()

    return skewness
def validate_dataset(df):

    if df.empty:
        raise ValueError("Dataset is empty")

    if df.shape[0] < 10:
        print("Warning: dataset has very few rows")

    return True
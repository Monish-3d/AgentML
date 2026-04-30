import pandas as pd

# A column is categorical if its unique values are less than this
# fraction of total rows - e.g. 0.5 means "less than 50% unique values"
CATEGORICAL_RATIO_THRESHOLD = 0.5


def detect_schema(df: pd.DataFrame) -> dict:
    """
    Classifies each column into one of four categories:
      - numeric:     int or float dtype
      - categorical: object dtype with low cardinality (few unique values relative to rows)
      - text:        object dtype with high cardinality (many unique values — free text)
      - datetime:    datetime dtype
    """

    schema = {
        "numeric": [],
        "categorical": [],
        "text": [],
        "datetime": [],
    }

    total_rows = len(df)

    for col in df.columns:

        if pd.api.types.is_numeric_dtype(df[col]):
            schema["numeric"].append(col)

        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            schema["datetime"].append(col)

        elif pd.api.types.is_object_dtype(df[col]):
            # Use ratio instead of raw count so the threshold
            # scales with dataset size
            ratio = df[col].nunique() / total_rows if total_rows > 0 else 0

            if ratio < CATEGORICAL_RATIO_THRESHOLD:
                schema["categorical"].append(col)
            else:
                schema["text"].append(col)

    return schema

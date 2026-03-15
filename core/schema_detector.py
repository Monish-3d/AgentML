import pandas as pd


def detect_schema(df):

    schema = {
        "numeric": [],
        "categorical": [],
        "text": []
    }

    for col in df.columns:

        if pd.api.types.is_numeric_dtype(df[col]):
            schema["numeric"].append(col)

        elif pd.api.types.is_object_dtype(df[col]):

            if df[col].nunique() < 50:
                schema["categorical"].append(col)

            else:
                schema["text"].append(col)

    return schema
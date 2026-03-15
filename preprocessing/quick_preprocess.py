import pandas as pd

def quick_encode(df):

    logs = []

    for col in list(df.columns):

        if pd.api.types.is_object_dtype(df[col]):

            values = df[col].dropna().str.lower().unique()
            n_unique = len(values)

            if set(values).issubset({"yes", "no"}):
                df[col] = df[col].str.lower().map({"yes": 1, "no": 0})
                logs.append(f"{col} → binary yes/no")

            elif set(values).issubset({"male", "female"}):
                df[col] = df[col].str.lower().map({"male": 1, "female": 0})
                logs.append(f"{col} → binary gender")

            elif n_unique == 2:
                vals = sorted(values)
                mapping = {v: i for i, v in enumerate(vals)}
                df[col] = df[col].str.lower().map(mapping)
                logs.append(f"{col} → binary mapping")

    return df, logs
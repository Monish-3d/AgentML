import pandas as pd

# Known binary mappings checked in order before the generic fallback
BINARY_MAPS = [
    ({"yes", "no"},         {"yes": 1, "no": 0},         "yes/no"),
    ({"true", "false"},     {"true": 1, "false": 0},      "true/false"),
    ({"male", "female"},    {"male": 1, "female": 0},     "male/female"),
    ({"on", "off"},         {"on": 1, "off": 0},          "on/off"),
    ({"1", "0"},            {"1": 1, "0": 0},             "string 1/0"),
]

def quick_encode(df: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    """
    Lightweight rule-based encoder for obvious binary columns.
    Returns a new DataFrame and a list of log messages.
    Only touches columns it can map completely — never silently introduces NaN.
    """

    df = df.copy()
    logs = []

    for col in df.columns:

        #  Case 1: actual boolean dtype (pandas parsed it as True/False)
        if pd.api.types.is_bool_dtype(df[col]):
            df[col] = df[col].astype(int)
            logs.append(f"[quick_encode] '{col}': bool dtype → 1/0")
            continue

        #  Case 2: object (string) dtype — check against known binary patterns
        if pd.api.types.is_object_dtype(df[col]):

            # Work only with non-null values, lowercased
            non_null = df[col].dropna()
            unique_vals = set(non_null.str.lower().unique())
            n_unique = len(unique_vals)

            # Skip if not exactly 2 unique values
            if n_unique != 2:
                continue

            # Check against every known pattern
            matched = False
            for known_set, mapping, label in BINARY_MAPS:
                if unique_vals == known_set:
                    encoded = df[col].str.lower().map(mapping)

                    # Safety check: mapping must not introduce new NaN values
                    original_nulls = df[col].isnull().sum()
                    new_nulls = encoded.isnull().sum()
                    if new_nulls > original_nulls:
                        logs.append(
                            f"[quick_encode] '{col}': skipped {label} mapping "
                            f"— introduced unexpected NaN values"
                        )
                        matched = True
                        break

                    df[col] = encoded
                    logs.append(f"[quick_encode] '{col}': {label} → 1/0")
                    matched = True
                    break

            # Generic 2-value fallback — alphabetical sort, clearly logged
            if not matched:
                vals = sorted(unique_vals)   # e.g. ["cat", "dog"] → cat=0, dog=1
                mapping = {v: i for i, v in enumerate(vals)}
                encoded = df[col].str.lower().map(mapping)

                # Safety check: no new NaN introduced
                original_nulls = df[col].isnull().sum()
                new_nulls = encoded.isnull().sum()
                if new_nulls > original_nulls:
                    logs.append(
                        f"[quick_encode] '{col}': skipped generic binary mapping "
                        f"— introduced unexpected NaN values"
                    )
                    continue

                df[col] = encoded
                logs.append(
                    f"[quick_encode] '{col}': generic binary → "
                    f"'{vals[0]}'=0, '{vals[1]}'=1"
                )

    return df, logs

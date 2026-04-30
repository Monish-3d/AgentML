import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
from imblearn.over_sampling import SMOTE

def apply_preprocessing(df, steps, target=None):

    df = df.copy()
    logs = []

    for step in steps:

        try:
            step_type = step.step

            # -----------------------
            # IMPUTE
            # -----------------------
            if step_type == "Impute":

                colms = step.columns
                method = step.method or "median"

                for col in colms:
                    if col not in df.columns:
                        logs.append(f"Skipped impute: {col} not found")
                        continue

                    if method == "mean":
                        df[col] = df[col].fillna(df[col].mean())
                    elif method == "median":
                        df[col] = df[col].fillna(df[col].median())
                    elif method == "mode":
                        df[col] = df[col].fillna(df[col].mode()[0])

                    logs.append(f"Imputed '{col}' using {method}")

            # -----------------------
            # TRANSFORM
            # -----------------------
            elif step_type == "Transform":

                colms = step.columns
                method = step.method

                for col in colms:
                    if col not in df.columns:
                        logs.append(f"Skipped transform: '{col}' not found")
                        continue

                    if method == "log":
                        df[col] = np.log1p(df[col])
                        logs.append(f"Log-transformed '{col}'")

            # -----------------------
            # ONE HOT ENCODING
            # -----------------------
            elif step_type == "One_Hot":

                for col in step.columns:
                    if col not in df.columns:
                        logs.append(f"Skipped OHE: '{col}' not found")
                        continue

                    df = pd.get_dummies(df, columns=[col])
                    logs.append(f"One-hot encoded '{col}'")

            # -----------------------
            # LABEL ENCODING
            # -----------------------
            elif step_type == "Encode":

                for col in step.columns:
                    if col not in df.columns:
                        logs.append(f"Skipped encode: '{col}' not found")
                        continue

                    le = LabelEncoder()
                    df[col] = le.fit_transform(df[col].astype(str))
                    logs.append(f"Label encoded '{col}'")

            # -----------------------
            # SCALING
            # -----------------------
            elif step_type == "Scale":

                valid_cols = [c for c in step.columns if c in df.columns]

                if not valid_cols:
                    logs.append("Skipped scaling: no valid columns found")
                    continue

                method = step.method or "standard"

                if method == "minmax":
                    scaler = MinMaxScaler()
                else:
                    scaler = StandardScaler()

                df[valid_cols] = scaler.fit_transform(df[valid_cols])
                logs.append(f"Scaled {valid_cols} using {method}")

            # -----------------------
            # SMOTE
            # -----------------------
            elif step_type == "SMOTE":

                if target is None or target not in df.columns:
                    logs.append("Skipped SMOTE: target not available")
                    continue

                X = df.drop(columns=[target])
                y = df[target]

                X = pd.get_dummies(X)

                sm = SMOTE()
                X_res, y_res = sm.fit_resample(X, y)

                df = pd.DataFrame(X_res, columns=X.columns)
                df[target] = y_res
                logs.append("Applied SMOTE")

            # -----------------------
            # DROP
            # -----------------------
            elif step_type == "Drop":

                for col in step.columns:
                    if col not in df.columns:
                        logs.append(f"Skipped drop: '{col}' not found")
                        continue

                    df = df.drop(columns=[col])
                    logs.append(f"Dropped column '{col}'")

            else:
                logs.append(f"Unknown step: {step_type}")

        except Exception as e:
            logs.append(f"Error in step '{step_type}': {str(e)}")

    return df, logs

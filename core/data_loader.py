import pandas as pd

def load_dataset(file):
    if file.endswith(".csv"):
        df = pd.read_csv(file)
    elif file.endswith(".xlsx"):
        df = pd.read_excel(file)
    else:
        raise ValueError(f"Unsupported file format")
    
    return df
    
    
def ask_metadata(df):

    print("Columns in dataset:\n")

    for i,col in enumerate(df.columns):
        print(f"{i}: {col}")

    target = input("\nEnter target column (or press enter if none): ")

    problem_type = None

    if target:
        problem_type = input("Problem type (classification/regression): ")

    return target, problem_type
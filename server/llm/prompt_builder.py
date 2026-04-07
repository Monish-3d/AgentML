def build_prompt(summary, missing, skewness, target, imbalance, corr):
    prompt = f"""
    You are a data preprocessing expert.

    Given the dataset information below, recommend preprocessing steps.

    DATASET SUMMARY:
    Rows: {summary['rows']}
    Columns: {summary['columns']}

    MISSING VALUES:
    {missing.to_dict()}

    SKEWNESS:
    {skewness}

    TARGET COLUMN:
    {target}

    CLASS IMBALANCE RATIO:
    {imbalance}

    CORRELATION MATRIX:
    {corr}
    """

    return prompt
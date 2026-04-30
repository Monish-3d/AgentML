def build_prompt(summary, missing, skewness, target, imbalance, corr, schema, problem_type, quick_logs):
    prompt = f"""
    You are a data preprocessing expert for machine learning workflows.

    Given the dataset information below, recommend a sequence of preprocessing steps.

    DATASET SUMMARY:
    - Rows: {summary['rows']}
    - Columns: {summary['columns']}
    - Column names: {summary['column_names']}

    PROBLEM TYPE: {problem_type}
    TARGET COLUMN: {target}

    SCHEMA (column type classifications):
    - Numeric columns:     {schema.get('numeric', [])}
    - Categorical columns: {schema.get('categorical', [])}
    - Text columns:        {schema.get('text', [])}
    - Datetime columns:    {schema.get('datetime', [])}

    ALREADY ENCODED (quick_encode already handled these — do NOT re-encode):
    {quick_logs if quick_logs else 'None'}

    MISSING VALUES (per column):
    {missing}

    SKEWNESS (numeric columns only):
    {skewness}

    CLASS IMBALANCE RATIO (majority / minority):
    {imbalance if imbalance is not None else 'N/A (regression task)'}

    CORRELATION MATRIX:
    {corr if corr is not None else 'Not enough numeric columns to compute'}
    """
    return prompt

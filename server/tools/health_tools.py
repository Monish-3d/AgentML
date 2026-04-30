def compute_health_score(df, skewness, imbalance_ratio=None):
    """
    Scores dataset quality from 0 to 100.

    Deductions:
    - Missing values  : tiered by severity     (up to -25)
    - Skewness        : capped total penalty   (up to -20)
    - Imbalance       : tiered by ratio        (up to -20)
    - Constant columns: useless for ML         (up to -10)
    - Duplicate rows  : data integrity issue   (up to -10)
    """

    score = 100
    total_cells = df.shape[0] * df.shape[1]

    # Missing values - tiered by overall missing ratio
    missing_ratio = df.isnull().sum().sum() / total_cells if total_cells > 0 else 0

    if missing_ratio > 0.30:
        score -= 25
    elif missing_ratio > 0.10:
        score -= 15
    elif missing_ratio > 0.02:
        score -= 5

    # Skewness - penalise per skewed column but cap total deduction at 20
    skew_penalty = sum(2 for val in skewness.values() if abs(val) > 1)
    score -= min(skew_penalty, 20)

    # Class imbalance
    if imbalance_ratio is not None:
        if imbalance_ratio > 10:
            score -= 20
        elif imbalance_ratio > 3:
            score -= 10

    # Constant columns (only one unique value — zero ML value)
    constant_cols = [col for col in df.columns if df[col].nunique(dropna=True) <= 1]
    score -= min(len(constant_cols) * 5, 10)

    # Duplicate rows
    duplicate_ratio = df.duplicated().sum() / df.shape[0] if df.shape[0] > 0 else 0
    if duplicate_ratio > 0.05:
        score -= 10
    elif duplicate_ratio > 0.01:
        score -= 5

    return max(score, 0)

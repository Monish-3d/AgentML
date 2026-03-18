def compute_health_score(df, skewness, imbalance_ratio=None):

    score = 100
    
    missing_ratio = df.isnull().sum().sum() / (df.shape[0] * df.shape[1])

    if missing_ratio > 0.1:
        score -= 10

    for val in skewness.values():

        if abs(val) > 1:
            score -= 2

    if imbalance_ratio and imbalance_ratio > 3:
        score -= 15

    return max(score, 0)
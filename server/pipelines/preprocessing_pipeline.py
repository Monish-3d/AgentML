from preprocessing.quick_preprocess import quick_encode
from core.schema_detector import detect_schema

from eda.eda_engine import dataset_summary, statistics, missing_values
from eda.distribution import compute_skewness
from eda.correlation import correlation_matrix
from eda.health_score import compute_health_score

from llm.prompt_builder import build_prompt
from llm.llm_client import get_preprocess_steps

from preprocessing.apply_pipeline import apply_preprocessing

def run_pipeline(df, target):

    logs = {}

    # -----------------------
    # 1. QUICK PREPROCESSING
    # -----------------------
    df, quick_logs = quick_encode(df)
    logs["quick_preprocessing"] = quick_logs

    # -----------------------
    # 2. SCHEMA
    # -----------------------
    schema = detect_schema(df)

    # -----------------------
    # 3. EDA
    # -----------------------
    summary = dataset_summary(df)
    stats = statistics(df)
    missing = missing_values(df)
    skewness = compute_skewness(df)
    corr = correlation_matrix(df)

    # -----------------------
    # 4. IMBALANCE
    # -----------------------
    imbalance = None
    if target and target in df.columns:
        counts = df[target].value_counts()
        if len(counts) > 1:
            imbalance = counts.max() / counts.min()

    # -----------------------
    # 5. HEALTH SCORE
    # -----------------------
    health = compute_health_score(df, skewness, imbalance)

    # -----------------------
    # 6. LLM RECOMMENDATION
    # -----------------------
    prompt = build_prompt(summary, missing, skewness, target, imbalance, corr)

    steps = get_preprocess_steps(prompt)

    logs["llm_steps"] = steps

    # -----------------------
    # 7. APPLY PREPROCESSING
    # -----------------------
    processed_df, apply_logs = apply_preprocessing(df, steps, target)

    logs["applied_steps"] = apply_logs

    return {
        "original_df": df,
        "processed_df": processed_df,
        "summary": summary,
        "stats": stats,
        "missing": missing,
        "skewness": skewness,
        "corr": corr,
        "health_score": health,
        "schema": schema,
        "steps": steps,
        "logs": logs
    }
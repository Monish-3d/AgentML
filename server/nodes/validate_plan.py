from workflow.state import AgentMLState

def validate_plan_node(state: AgentMLState) -> AgentMLState:

    recommended_steps = state.get("recommended_steps", [])
    df = state.get("df")
    problem_type = state.get("problem_type", "")
    warnings = []

    # Nothing to validate
    if not recommended_steps or df is None:
        return {
            "validated_steps": [], "validation_warnings": warnings,
            "current_node": "validate_plan", "progress": 72,
        }

    df_columns = set(df.columns)
    validated = []

    for step in recommended_steps:
        step_type = step.step

        # Skip
        if step_type == "Skip":
            continue

        # SMOTE only makes sense for classification
        if step_type == "SMOTE":
            if problem_type != "classification":
                warnings.append("SMOTE skipped — only valid for classification tasks.")
                continue
            validated.append(step)
            continue

        # For all other steps, validate that the columns exist in the df
        if not step.columns:
            warnings.append(f"Step '{step_type}' skipped — no columns specified.")
            continue

        valid_cols = [col for col in step.columns if col in df_columns]
        missing_cols = [col for col in step.columns if col not in df_columns]

        if missing_cols:
            warnings.append(
                f"Step '{step_type}': columns {missing_cols} not found in dataset — skipped for those columns."
            )

        if not valid_cols:
            warnings.append(f"Step '{step_type}' skipped entirely — none of its columns exist.")
            continue

        # Rebuild step with only the valid columns
        step.columns = valid_cols
        validated.append(step)

    return {
        "validated_steps": validated, "validation_warnings": warnings,
        "current_node": "validate_plan", "progress": 72,
    }

from llm.prompts import build_prompt
from workflow.state import AgentMLState


def prompt_build_node(state: AgentMLState) -> AgentMLState:

    if state.get("df") is None:
        return {"current_node": "prompt_build", "progress": 55, "llm_prompt": ""}

    prompt = build_prompt(
        summary = state["summary"],
        missing = state["missing_json"],
        skewness = state["skewness"],
        target = state["target"],
        imbalance = state.get("imbalance_ratio"),
        corr = state.get("correlation_json"),
        schema = state["schema"],
        problem_type = state["problem_type"],
        quick_logs=state.get("quick_logs", []),
    )

    return {
        "llm_prompt": prompt,
        "current_node": "prompt_build",
        "progress": 55,
    }

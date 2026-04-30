from workflow.state import AgentMLState
from typing import Literal

def check_validate_node(state: AgentMLState) -> Literal["exists", "empty"]:
    # Use falsy check- validated_steps will be [] (empty list), not None
    if not state.get("validated_steps"):
        return "empty"
    return "exists"

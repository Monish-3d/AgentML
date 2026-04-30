from workflow.state import AgentMLState
from tools.schema_tools import detect_schema

def schema_detect_node(state: AgentMLState) -> AgentMLState:

    #if ingest_node failed return empty schema
    if state.get("df") is None:
        return {"current_node": "schema_detect", "progress": 30, "schema": {}}

    schema = detect_schema(state["df"])

    return {
        "schema": schema, "current_node": "schema_detect", "progress": 30}

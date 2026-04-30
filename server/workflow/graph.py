from langgraph.graph import StateGraph, START, END
from workflow.state import AgentMLState
from nodes.ingest import ingest_node
from nodes.quick_preprocess import quick_preprocess_node
from nodes.schema_detect import schema_detect_node
from nodes.eda import eda_node
from nodes.prompt_build import prompt_build_node
from nodes.llm_recommend import llm_recommend_node
from nodes.validate_plan import validate_plan_node
from nodes.apply_preprocessing import apply_preprocessing_node
from nodes.health_explain import health_explain_node
from nodes.output import output_node
from workflow.edges import check_validate_node

graph = StateGraph(AgentMLState)

graph.add_node('ingest_node', ingest_node)
graph.add_node('quick_preprocess_node', quick_preprocess_node)
graph.add_node('schema_detect_node', schema_detect_node)
graph.add_node('eda_node', eda_node)
graph.add_node('prompt_build_node', prompt_build_node)
graph.add_node('llm_recommend_node', llm_recommend_node)
graph.add_node('validate_plan_node', validate_plan_node)
graph.add_node('apply_preprocessing_node', apply_preprocessing_node)
graph.add_node('health_explain_node', health_explain_node)
graph.add_node('output_node', output_node)

graph.add_edge(START, 'ingest_node')
graph.add_edge('ingest_node', 'quick_preprocess_node')
graph.add_edge('quick_preprocess_node', 'schema_detect_node')
graph.add_edge('schema_detect_node', 'eda_node')
graph.add_edge('eda_node', 'prompt_build_node')
graph.add_edge('prompt_build_node', 'llm_recommend_node')
graph.add_edge('llm_recommend_node', 'validate_plan_node')

graph.add_conditional_edges('validate_plan_node', check_validate_node, {'exists': 'apply_preprocessing_node', 'empty': 'health_explain_node'})

graph.add_edge('apply_preprocessing_node', 'health_explain_node')
graph.add_edge('health_explain_node', 'output_node')
graph.add_edge('output_node', END)

workflow = graph.compile()

#-------------------quick-workflow-check---------------------------------

# png_data = workflow.get_graph().draw_mermaid_png()

# with open("workflow_graph.png", "wb") as f:
#     f.write(png_data)

# print("Graph saved as workflow_graph.png")
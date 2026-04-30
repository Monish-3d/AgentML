import asyncio
from workflow.graph import workflow
from core.data_loader import load_dataset
from jobs import registry


async def execute_graph(job_id: str, file_path: str, target: str, problem_type: str, filename: str):

    registry.update_job(job_id, status="running")

    try:
        df = load_dataset(file_path)

        initial_state = {
            "job_id": job_id,
            "raw_df": df,
            "df": None,
            "processed_df": None,
            "target": target,
            "problem_type": problem_type,
            "filename": filename,
            "errors": [],
        }

        # stream() yields {node_name: node_output_dict} after each node finishes
        # This lets us update the registry with live current_node and progress
        final_state = {}

        def run_stream():
            for chunk in workflow.stream(initial_state):
                # chunk is {"node_name": {state fields the node returned}}
                node_output = list(chunk.values())[0]
                registry.update_job(
                    job_id,
                    current_node=node_output.get("current_node", ""),
                    progress=node_output.get("progress", 0),
                )
                # Accumulate state so we have the full picture at the end
                final_state.update(node_output)

        await asyncio.to_thread(run_stream)

        registry.update_job(
            job_id,
            status="completed",
            output_path=final_state.get("output_path", ""),
            result={
                "summary":              final_state.get("summary", {}),
                "dataset_schema":       final_state.get("schema", {}),
                "missing":              final_state.get("missing_json", {}),
                "stats":                final_state.get("stats_json", {}),
                "skewness":             final_state.get("skewness", {}),
                "correlation":          final_state.get("correlation_json"),
                "imbalance_ratio":      final_state.get("imbalance_ratio"),
                "health_score":         final_state.get("health_score", 0),
                "health_explanation":   final_state.get("health_explanation", ""),
                "quick_logs":           final_state.get("quick_logs", []),
                "recommended_steps":    [s.dict() for s in final_state.get("recommended_steps", [])],
                "validated_steps":      [s.dict() for s in final_state.get("validated_steps", [])],
                "validation_warnings":  final_state.get("validation_warnings", []),
                "apply_logs":           final_state.get("apply_logs", []),
                "errors":               final_state.get("errors", []),
            },
        )

    except Exception as e:
        registry.update_job(job_id, status="failed", error=str(e))

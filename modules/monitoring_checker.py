from srebuddy.ragflow_manager import get_pipeline


def check_monitoring_implementation(code_snippet):
    pipeline = get_pipeline("srebuddy/configs/ragflow_config.yaml")
    query = f"Check if monitoring is implemented properly in this code: {code_snippet}"
    result = pipeline.run(query)
    return result["answer"]

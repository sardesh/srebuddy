from srebuddy.ragflow_manager import get_pipeline
import sys
import os
os.environ["OMP_NUM_THREADS"] = "1"
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))


def test_query_sre_practices():
    pipeline = get_pipeline("configs/ragflow_config.yaml")
    query = "What SRE practices are being implemented in GoogleCloudPlatform/microservices-demo?"
    result = pipeline.run(query)
    print("\nRAG Agent Answer:\n", result["answer"])
    assert result["answer"], "RAG agent did not return an answer."


if __name__ == "__main__":
    test_query_sre_practices()

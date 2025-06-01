
from ragflow.pipeline import RAGPipeline
import yaml

def load_ragflow_config(config_path):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def get_pipeline(config_path):
    config = load_ragflow_config(config_path)
    return RAGPipeline.from_config(config)

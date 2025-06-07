import yaml
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import openai
import os


def load_ragflow_config(config_path):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def get_pipeline(config_path):
    config = load_ragflow_config(config_path)
    embedding_model = config['retriever']['embedding_model']
    index_path = config['retriever']['index_path']
    meta_path = index_path + '.meta.yaml'
    model = SentenceTransformer(embedding_model)
    index = faiss.read_index(index_path)
    with open(meta_path, 'r') as f:
        meta = yaml.safe_load(f)
    chunks = meta['chunks']
    metadatas = meta['metadatas']
    openai_api_key = os.getenv('OPENAI_API_KEY')
    openai_model = config.get('generator', {}).get('model', 'gpt-4')
    temperature = config.get('generator', {}).get('temperature', 0.0)
    client = openai.OpenAI(api_key=openai_api_key)

    class RealRAGPipeline:
        def run(self, query, top_k=5):
            query_emb = model.encode([query])
            D, I = index.search(np.array(query_emb).astype('float32'), top_k)
            retrieved = [chunks[i] for i in I[0]]
            context = '\n---\n'.join(retrieved)
            prompt = f"""
You are an SRE expert. Given the following documentation and code context from a repository, extract and summarize the SRE practices being implemented. List them clearly and concisely.

Context:
{context}

Question: {query}

Answer as a bullet list:
"""
            response = client.chat.completions.create(
                model=openai_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=400
            )
            answer = response.choices[0].message.content.strip()
            return {"answer": answer}
    return RealRAGPipeline()

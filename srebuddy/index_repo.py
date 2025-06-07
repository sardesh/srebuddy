import os
import sys
import tempfile
import shutil
from pathlib import Path
import requests
import zipfile
from sentence_transformers import SentenceTransformer
import faiss
import yaml

CONFIG_PATH = os.path.join(os.path.dirname(
    __file__), '../configs/ragflow_config.yaml')

# Load config


def load_config():
    with open(CONFIG_PATH, 'r') as f:
        return yaml.safe_load(f)

# Download and extract GitHub repo as zip


def download_github_repo(repo_url, extract_to):
    if repo_url.endswith('/'):
        repo_url = repo_url[:-1]
    repo_name = repo_url.split('/')[-1]
    zip_url = repo_url + '/archive/refs/heads/main.zip'
    r = requests.get(zip_url)
    zip_path = os.path.join(extract_to, f'{repo_name}.zip')
    with open(zip_path, 'wb') as f:
        f.write(r.content)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    os.remove(zip_path)
    # Return path to extracted repo
    for entry in os.listdir(extract_to):
        if os.path.isdir(os.path.join(extract_to, entry)) and repo_name in entry:
            return os.path.join(extract_to, entry)
    return None

# Collect text from code and markdown files


def collect_text_files(root_dir, exts=(".py", ".md", ".yaml", ".yml")):
    texts = []
    for dirpath, _, filenames in os.walk(root_dir):
        for fname in filenames:
            if fname.endswith(exts):
                fpath = os.path.join(dirpath, fname)
                try:
                    with open(fpath, 'r', encoding='utf-8') as f:
                        texts.append(f.read())
                except Exception:
                    continue
    return texts

# Chunk text for embedding


def chunk_text(text, chunk_size=512, overlap=64):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = ' '.join(words[i:i+chunk_size])
        if chunk:
            chunks.append(chunk)
    return chunks

# Main indexing function


def index_repo_and_fisas(repo_url):
    config = load_config()
    embedding_model = config['retriever']['embedding_model']
    index_path = config['retriever']['index_path']
    document_source = config['retriever']['document_source']

    model = SentenceTransformer(embedding_model)
    all_chunks = []
    all_metadatas = []

    # Index FISAS DB (sre_standards.md)
    fisas_path = os.path.join(document_source, 'sre_standards.md')
    with open(fisas_path, 'r', encoding='utf-8') as f:
        fisas_text = f.read()
    fisas_chunks = chunk_text(fisas_text)
    all_chunks.extend(fisas_chunks)
    all_metadatas.extend([{'source': 'fisas_db'} for _ in fisas_chunks])

    # Index GitHub repo
    with tempfile.TemporaryDirectory() as tmpdir:
        repo_dir = download_github_repo(repo_url, tmpdir)
        if not repo_dir:
            print('Failed to download or extract repo.')
            return
        repo_texts = collect_text_files(repo_dir)
        for text in repo_texts:
            chunks = chunk_text(text)
            all_chunks.extend(chunks)
            all_metadatas.extend(
                [{'source': 'repo', 'repo_url': repo_url} for _ in chunks])

    # Embed and store in FAISS
    print(f'Embedding {len(all_chunks)} chunks...')
    embeddings = model.encode(all_chunks, show_progress_bar=True)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    os.makedirs(os.path.dirname(index_path), exist_ok=True)
    faiss.write_index(index, index_path)
    print(f'Index written to {index_path}')

    # Optionally, save metadatas and chunks for lookup
    with open(index_path + '.meta.yaml', 'w') as f:
        yaml.dump({'chunks': all_chunks, 'metadatas': all_metadatas}, f)
    print('Metadata written.')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python index_repo.py <github_repo_url>')
        sys.exit(1)
    repo_url = sys.argv[1]
    index_repo_and_fisas(repo_url)

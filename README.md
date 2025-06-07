# SreBuddy with RAGFlow 🔥

A Retrieval-Augmented Generation (RAG) powered agent with access to FISAS DB data (stored as part of this project) to scan repositories and suggest missing SRE implementations like logging, monitoring, alerting, and Dynatrace agent checks based on in-house standards.

## 📦 Features

- Modular SRE checks (logging, monitoring, alerting, Dynatrace)
- RAG Agent based storage for repositoryis for bitbucket or github for vector db
- OpenAI GPT-4 powered code suggestions
- Configurable pipeline via YAML

## 🚀 Run Instructions

1️⃣ Create and activate a Python virtual environment (recommended):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2️⃣ Install requirements:

```bash
pip install -r requirements.txt
```

3️⃣ Prepare vector index (RAGFlow utility):

```bash
python srebuddy/index_repo.py <github_repo_url>
```

4️⃣ Run test:

```bash
python srebuddy/test_rag_query.py
```

5️⃣ (Optional) Run the main check:

```bash
python srebuddy/srebuddy/run_ragflow.py
```

6️⃣ Review results and suggested implementation snippets.

## 📊 Extending

Add new modules in `srebuddy/modules/`, update prompt and config — plug and play!

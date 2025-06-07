# SreBuddy with RAGFlow 🔥

A Retrieval-Augmented Generation (RAG) powered agent with access to FISAS DB data (stored as part of this project) to scan repositories and suggest missing SRE implementations like logging, monitoring, alerting, and Dynatrace agent checks based on in-house standards.

## 📦 Features

- Modular SRE checks (logging, monitoring, alerting, Dynatrace)
- RAG Agent based storage for repositoryis for bitbucket or github for vector db
- OpenAI GPT-4 powered code suggestions
- Configurable pipeline via YAML

## 🚀 Run Instructions

1️⃣ Install requirements:

```bash
pip install -r requirements.txt
```

2️⃣ Prepare vector index (RAGFlow utility)

3️⃣ Run check:

```bash
python srebuddy/srebuddy/run_ragflow.py
```

4️⃣ Review results and suggested implementation snippets.

## 📊 Extending

Add new modules in `srebuddy/modules/`, update prompt and config — plug and play!

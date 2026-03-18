# AWS Semantic Threat Hunter 🛡️

An AI-powered security tool that uses Natural Language Processing (NLP) to hunt through AWS CloudTrail logs.

## Features
- **Semantic Search:** Move beyond keyword matching. Hunt for "unauthorized activity" or "secret access" using intent.
- **Local AI:** Uses `Sentence-Transformers` to vectorize logs locally (no data sent to 3rd party AI).
- **High Performance:** Utilizes `FAISS` for sub-millisecond vector similarity search.
- **Live Dashboard:** Interactive UI built with `Streamlit` for real-time analysis.

## Tech Stack
- **Cloud:** AWS (S3, CloudTrail, IAM, Boto3)
- **AI/ML:** Sentence-Transformers (`all-MiniLM-L6-v2`), FAISS
- **Backend:** Python
- **Frontend:** Streamlit

## Project Structure
- `fetch_logs.py`: Recursive log retrieval from S3.
- `process_vectors.py`: Converts JSON logs into a mathematical vector index.
- `app.py`: The Streamlit dashboard interface.
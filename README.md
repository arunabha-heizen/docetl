# Document Verification Microservice

A production-grade Python microservice for parsing, analyzing, and verifying legal documents.

## Features
- **Document Parsing**: Uses `docling` to convert PDF/HTML to structured text.
- **Analysis**: Uses `docetl` (simulated via LLM) to classify documents and extract entities.
- **Verification**: configurable rule engine that checks extracted data against a knowledge base.
- **Configurable**: All rules and document types are defined in `config/rules.json`.

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Variables**:
   Create a `.env` file:
   ```
   ANTHROPIC_API_KEY=your_api_key
   MODEL_NAME=claude-3-5-haiku-20241022
   ```

3. **Run Server**:
   ```bash
   uvicorn app.main:app --reload
   ```

## Usage

Send a POST request to `/api/v1/verify`:

```bash
curl -X POST "http://localhost:8000/api/v1/verify" \
  -F "file=@/path/to/doc.pdf" \
  -F "name=Board Consent" \
  -F "id=123" \
  -F "workflow_type=INCREASE_AUTHORIZED_SHARES"
```

## Docker

```bash
docker-compose up --build
```

import json
import os
import tempfile
import boto3
from urllib.parse import urlparse
from app.core.parser import Parser
from app.core.analyzer import Analyzer
from dotenv import load_dotenv

load_dotenv()

s3_client = boto3.client('s3')
parser = Parser()
analyzer = Analyzer()

def lambda_handler(event, context):
    """
    AWS Lambda Handler
    Event payload:
    {
        "s3_url": "s3://bucket/key",
        "document_name": "example.pdf",
        "id": "123",
        "workflow": "lease_agreement"
    }
    """
    print(f"Received event: {json.dumps(event)}")
    
    s3_url = event.get("s3_url")
    doc_name = event.get("document_name")
    doc_id = event.get("id")
    workflow = event.get("workflow")
    
    if not s3_url:
        return {"error": "s3_url is required"}

    # Parse S3 URL
    parsed_url = urlparse(s3_url)
    bucket_name = parsed_url.netloc
    object_key = parsed_url.path.lstrip('/')
    
    tmp_path = None
    try:
        # Download file to /tmp
        suffix = os.path.splitext(object_key)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            print(f"Downloading {s3_url} to {tmp.name}")
            s3_client.download_file(bucket_name, object_key, tmp.name)
            tmp_path = tmp.name
            
        # 1. Parse using Docling
        print("Parsing document...")
        markdown_content = parser.parse_file(tmp_path)
        
        # 2. Analyze using DocETL (simulated)
        print("Analyzing document...")
        analysis_result = analyzer.analyze(markdown_content, workflow)
        
        return {
            "status": "success",
            "id": doc_id,
            "document_name": doc_name,
            "workflow": workflow,
            "data": analysis_result["extraction"],
            "doc_type": analysis_result["doc_type"],
            "usage": analysis_result.get("usage")
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            "status": "error",
            "message": str(e)
        }
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)

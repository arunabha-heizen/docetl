from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.api.models import VerifyRequest, VerificationResult, WorkflowType
from app.core.parser import Parser
from app.core.analyzer import Analyzer
from app.core.verifier import Verifier
import tempfile
import os
import shutil

router = APIRouter()

parser = Parser()
analyzer = Analyzer()
verifier = Verifier()

@router.post("/verify", response_model=VerificationResult)
async def verify_document(
    file: UploadFile = File(...),
    name: str = Form(...),
    id: str = Form(...),
    workflow_type: WorkflowType = Form(...)
):
    # 1. Save file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    try:
        # 2. Parse Document
        markdown_content = parser.parse_file(tmp_path)
        
        # 3. Analyze (Classify & Extract)
        analysis_result = analyzer.analyze(markdown_content, workflow_type)
        doc_type = analysis_result["doc_type"]
        extraction = analysis_result["extraction"]
        
        # 4. Verify
        verification_result = verifier.verify(doc_type, extraction, workflow_type)
        
        return VerificationResult(
            status=verification_result.get("status", "WARNING"),
            checks=verification_result.get("checks", []),
            extracted_data=extraction,
            message=verification_result.get("message")
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

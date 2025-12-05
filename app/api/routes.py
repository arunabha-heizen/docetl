from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.api.models import VerifyRequest, VerificationResult, WorkflowType, ServerlessMetrics, AdvancedMetrics
from app.core.parser import Parser
from app.core.analyzer import Analyzer
from app.core.verifier import Verifier
from app.core.monitor import ResourceMonitor
import tempfile
import os
import shutil
import time

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
    start_wall = time.time()
    start_cpu = time.process_time()

    # 1. Save file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    try:
        with ResourceMonitor() as monitor:
            # 2. Parse Document
            markdown_content = parser.parse_file(tmp_path)
            
            # 3. Analyze (Classify & Extract)
            analysis_result = analyzer.analyze(markdown_content, workflow_type)
            doc_type = analysis_result["doc_type"]
            extraction = analysis_result["extraction"]
            usage = analysis_result.get("usage")
            
            # 4. Verify
            verification_result = verifier.verify(doc_type, extraction, workflow_type)
        
        end_wall = time.time()
        end_cpu = time.process_time()
        
        metrics = ServerlessMetrics(
            cpu_time_seconds=round(end_cpu - start_cpu, 4),
            wall_time_seconds=round(end_wall - start_wall, 4)
        )
        
        adv_metrics = AdvancedMetrics(**monitor.get_metrics())
        
        return VerificationResult(
            status=verification_result.get("status", "WARNING"),
            checks=verification_result.get("checks", []),
            extracted_data=extraction,
            message=verification_result.get("message"),
            markdown_content=markdown_content,
            usage=usage,
            metrics=metrics,
            advanced_metrics=adv_metrics
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

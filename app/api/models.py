from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class WorkflowType(str, Enum):
    NONE = "NONE"
    INCREASE_AUTHORIZED_SHARES = "INCREASE_AUTHORIZED_SHARES"
    INCREASE_STOCK_OPTION_PLAN = "INCREASE_STOCK_OPTION_PLAN"
    CREATE_STOCK_OPTION_PLAN = "CREATE_STOCK_OPTION_PLAN"
    AUTHORIZED_ROUND = "AUTHORIZED_ROUND"
    SAFE_ROUND = "SAFE_ROUND"
    PROMISE_GRANT = "PROMISE_GRANT"
    COMPANY_SERVICE_PROVIDER = "COMPANY_SERVICE_PROVIDER"
    ISSUE_INDIVIDUAL_ROUND = "ISSUE_INDIVIDUAL_ROUND"
    ISSUE_INDIVIDUAL_SAFE = "ISSUE_INDIVIDUAL_SAFE"
    INCREASE_AUTHORIZED_ROUND = "INCREASE_AUTHORIZED_ROUND"
    INCREASE_AUTHORIZED_SAFE_ROUND = "INCREASE_AUTHORIZED_SAFE_ROUND"
    RECORD_AUTHORIZED_ROUND = "RECORD_AUTHORIZED_ROUND"
    RECORD_AUTHORIZED_SAFE_ROUND = "RECORD_AUTHORIZED_SAFE_ROUND"
    REPURCHASE_INDIVIDUAL_SAFE = "REPURCHASE_INDIVIDUAL_SAFE"
    SAFE_REPURCHASE = "SAFE_REPURCHASE"
    RECORD_ISSUE_INDIVIDUAL_NOTE = "RECORD_ISSUE_INDIVIDUAL_NOTE"
    RECORD_ISSUE_INDIVIDUAL_SAFE_NOTE = "RECORD_ISSUE_INDIVIDUAL_SAFE_NOTE"
    VALUATION_409A = "VALUATION_409A"
    TERMINATE_COMPANY_SERVICE_PROVIDER = "TERMINATE_COMPANY_SERVICE_PROVIDER"
    EXERCISE_STOCK_OPTION = "EXERCISE_STOCK_OPTION"
    COMMON_STOCK_ISSUE = "COMMON_STOCK_ISSUE"
    STOCK_OPTION_ISSUE = "STOCK_OPTION_ISSUE"
    STOCK_OPTION_REDUCE = "STOCK_OPTION_REDUCE"
    TERMINATE_OFFICERS = "TERMINATE_OFFICERS"
    PRE_INCORPORATION = "PRE_INCORPORATION"

class DocumentMetadata(BaseModel):
    name: str
    id: str
    workflow_type: WorkflowType

class TokenUsage(BaseModel):
    input_tokens: int
    output_tokens: int
    total_tokens: int
    estimated_cost: float

class ServerlessMetrics(BaseModel):
    cpu_time_seconds: float
    wall_time_seconds: float

class AdvancedMetrics(BaseModel):
    peak_memory_mb: float
    peak_cpu_usage_percent: float
    avg_cpu_usage_percent: float
    active_core_count: int

class VerificationResult(BaseModel):
    status: str  # "CLEARED", "WARNING", "FAILED"
    checks: List[Dict[str, Any]]
    extracted_data: Dict[str, Any]
    message: Optional[str] = None
    markdown_content: str
    usage: Optional[TokenUsage] = None
    metrics: Optional[ServerlessMetrics] = None
    advanced_metrics: Optional[AdvancedMetrics] = None

class VerifyRequest(BaseModel):
    document_content: str # Base64 encoded or path? The user said "Request will send document its name, id and workflow type". 
                          # Usually file upload is separate. I'll assume this model is for the JSON part, 
                          # and the file is sent as Multipart/Form-Data.
    metadata: DocumentMetadata

# For the actual API endpoint, we'll use UploadFile for the document.

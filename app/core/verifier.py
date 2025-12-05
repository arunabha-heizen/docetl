from typing import Dict, Any, List
from app.config.settings import settings
import anthropic

class Verifier:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        self.model = settings.model_name
        self.workflows = settings.rules["workflows"]
        self.knowledge_base = settings.rules["knowledge_base"]

    def verify(self, doc_type: str, extraction: Dict[str, Any], workflow_type: str) -> Dict[str, Any]:
        """
        Verifies the extracted data against the workflow rules and knowledge base.
        """
        
        workflow_rules = self.workflows.get(workflow_type, {})
        required_docs = workflow_rules.get("required_documents", [])
        verification_rules = workflow_rules.get("verification_rules", [])
        
        # 1. Check if doc_type is valid for this workflow
        # Note: The request is for a single document, but a workflow might require multiple.
        # We check if the current doc is ONE OF the required ones.
        # Or if the workflow implies checking this specific doc.
        
        doc_valid = doc_type in required_docs if required_docs else True
        # If required_docs is empty, maybe it's a generic workflow or we just check rules.
        
        # 2. Verify Rules using LLM
        # We construct a prompt with the rules and the extraction.
        
        kb_context = "\n".join([f"{k}: {v}" for k, v in self.knowledge_base.items()])
        
        prompt = f"""
        You are a legal compliance verifier.
        
        Workflow: {workflow_type}
        Document Type: {doc_type}
        
        Extracted Data:
        {extraction}
        
        Verification Rules:
        {json.dumps(verification_rules, indent=2)}
        
        Knowledge Base:
        {kb_context}
        
        Task:
        1. Check if the document type '{doc_type}' is appropriate for this workflow.
        2. Verify if the extracted data conforms to the Verification Rules and Knowledge Base.
        3. Identify any missing signatures, dates, or required clauses.
        
        Return a JSON object with:
        - status: "CLEARED" | "WARNING" | "FAILED"
        - checks: List of objects {{ "rule": str, "status": "PASS"|"FAIL", "reason": str }}
        - message: Overall summary.
        """
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        try:
            text = response.content[0].text
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]
            return json.loads(text)
        except:
             return {
                 "status": "WARNING",
                 "checks": [],
                 "message": "Could not parse verification result.",
                 "raw": response.content[0].text
             }

import json

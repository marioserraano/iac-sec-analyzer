import json
from typing import Any, Dict
from iac_sec.core.config import settings
from iac_sec.models.schemas import SecurityReport
from iac_sec.analyzer.llm_client import get_llm_client

class SecurityAnalyzer:
    """
    Core engine that orchestrates the analysis of parsed IaC code.
    It builds the context, queries the local LLM, and returns a validated Pydantic model.
    """
    
    def __init__(self, filename: str):
        self.filename = filename
        self.client = get_llm_client()
        self.model = settings.LLM_MODEL
        
    def _build_system_prompt(self) -> str:
        """Constructs a highly constrained system prompt for the DevSecOps role."""
        return (
            "You are a Senior Cloud Security Architect and DevSecOps Engineer. "
            "Your task is to analyze the provided Terraform (HCL) JSON representation "
            "and identify security misconfigurations, focusing on:\n"
            "1. Excessive IAM permissions (e.g., wildcard '*' actions).\n"
            "2. Publicly exposed resources (e.g., 0.0.0.0/0 in Security Groups).\n"
            "3. Lack of encryption at rest (S3, RDS, EBS) or in transit.\n"
            "4. Hardcoded secrets or plain-text credentials.\n\n"
            "RULES:\n"
            "- ONLY report actual security vulnerabilities.\n"
            "- Be concise but highly technical in your descriptions.\n"
            "- Provide actionable remediation steps.\n"
            "- You MUST return the output strictly adhering to the requested JSON schema."
        )

    async def analyze(self, parsed_hcl: Dict[str, Any]) -> SecurityReport:
        """Sends the parsed HCL to the local LLM and forces a structured response."""
        system_prompt = self._build_system_prompt()
        iac_context = json.dumps(parsed_hcl, indent=2)
        
        report: SecurityReport = await self.client.chat.completions.create(
            model=self.model,
            response_model=SecurityReport,
            temperature=0.0,
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user", 
                    "content": f"Analyze the following Terraform code from file '{self.filename}':\n\n{iac_context}"
                }
            ]
        )
        
        report.file_name = self.filename
        return report
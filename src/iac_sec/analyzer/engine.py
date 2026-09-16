import json
from typing import Any, Dict, Optional
from iac_sec.core.config import settings
from iac_sec.models.schemas import SecurityReport
from iac_sec.analyzer.llm_client import get_llm_client

class SecurityAnalyzer:
    """
    Core engine that orchestrates the analysis of parsed IaC code.
    It builds the context, queries the local LLM, and returns a validated Pydantic model.
    """
    
    def __init__(self, filename: str, custom_policy: Optional[str] = None):
        self.filename = filename
        self.custom_policy = custom_policy
        self.client = get_llm_client()
        self.model = settings.LLM_MODEL
        
    def _build_system_prompt(self) -> str:
        """Constructs a highly constrained system prompt for the DevSecOps role."""
        prompt = (
            "You are a Senior Cloud Security Architect. Your task is to exhaustively analyze "
            "the provided Terraform JSON and identify ALL security misconfigurations AND policy violations.\n\n"
            "MANDATORY CHECKLIST (You MUST evaluate all of these):\n"
            "1. PROVIDERS: Look for hardcoded secrets (access_key, secret_key).\n"
            "2. IAM: Look for wildcard '*' actions or overly permissive policies in 'resource' blocks.\n"
            "3. NETWORKING: Look for publicly exposed ports (e.g., 0.0.0.0/0 in ingress) in 'resource' blocks.\n"
            "4. STORAGE: Look for unencrypted S3 buckets, RDS, or EBS in 'resource' blocks.\n"
        )

        # RAG: Trigger-Action pattern
        if self.custom_policy:
            prompt += (
                "5. CUSTOM COMPANY POLICIES:\n"
                f"   - Rule: {self.custom_policy}\n"
                "   - ACTION: You MUST check all resources against this rule. If a resource violates this rule, report it as a vulnerability.\n"
            )

        prompt += (
            "\nRULES:\n"
            "- Scan the ENTIRE JSON meticulously from top to bottom, starting with the providers.\n"
            "- Report BOTH general security vulnerabilities AND violations of the custom policies.\n"
            "- Be concise but highly technical.\n"
            "- You MUST return the output strictly adhering to the requested JSON schema."
        )

        return prompt

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
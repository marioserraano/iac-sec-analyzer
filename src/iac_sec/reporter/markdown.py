from iac_sec.models.schemas import SecurityReport

class MarkdownReporter:
    """Generates a Markdown representation of the security report for CI/CD systems."""
    
    @staticmethod
    def generate(report: SecurityReport) -> str:
        """Translates the Pydantic model into a Markdown string."""
        lines = [
            f"# 🛡️ IaC Security Report: `{report.file_name}`",
            f"**Total Issues Found:** {report.total_issues_found}",
            "---",
            "## 🚨 Vulnerabilities" if report.total_issues_found > 0 else "## ✅ No vulnerabilities found!"
        ]

        for vuln in report.vulnerabilities:
            lines.append(f"### {vuln.rule_id} - {vuln.resource_name}")
            lines.append(f"- **Severity:** `{vuln.severity.value}`")
            lines.append(f"- **Line:** {vuln.line_number if vuln.line_number else 'N/A'}")
            lines.append(f"- **Description:** {vuln.description}")
            lines.append(f"- **Remediation:** {vuln.remediation}")
            lines.append("") # Empty line for spacing

        return "\n".join(lines)
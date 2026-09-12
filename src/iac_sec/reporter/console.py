from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from iac_sec.models.schemas import SecurityReport, SeverityLevel

# Instantiate a global console object for rich text printing
console = Console()

class ConsoleReporter:
    """
    Handles the formatting and display of the security report in the terminal.
    Uses the 'rich' library to render beautiful tables and panels.
    """
    
    @staticmethod
    def print_report(report: SecurityReport) -> None:
        """
        Renders the validation results.
        
        Args:
            report (SecurityReport): The validated Pydantic model from the LLM.
        """
        # 1. Print the header panel
        header_text = (
            f"[bold cyan]File Analyzed:[/bold cyan] {report.file_name}\n"
            f"[bold cyan]Total Issues Found:[/bold cyan] {report.total_issues_found}"
        )
        
        panel_color = "red" if report.total_issues_found > 0 else "green"
        console.print(Panel(header_text, title="IaC Security Report", border_style=panel_color))
        
        if report.total_issues_found == 0:
            console.print("\n[bold green]✅ No security vulnerabilities detected. Great job![/bold green]\n")
            return

        # 2. Build the vulnerabilities table
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Rule ID", style="dim", width=12)
        table.add_column("Severity", justify="center")
        table.add_column("Resource", style="cyan")
        table.add_column("Line")
        table.add_column("Description")
        
        # 3. Populate the table rows
        for vuln in report.vulnerabilities:
            # Color-code the severity dynamically
            sev_color = "red" if vuln.severity in [SeverityLevel.CRITICAL, SeverityLevel.HIGH] else "yellow"
            
            line_str = str(vuln.line_number) if vuln.line_number else "N/A"
            
            table.add_row(
                vuln.rule_id,
                f"[{sev_color}]{vuln.severity.value}[/{sev_color}]",
                vuln.resource_name,
                line_str,
                vuln.description
            )
            
        # 4. Print the table and remediation steps
        console.print(table)
        
        console.print("\n[bold underline]Remediation Steps:[/bold underline]")
        for vuln in report.vulnerabilities:
            console.print(f"- [bold]{vuln.rule_id}[/bold]: {vuln.remediation}")
        console.print()  # Extra newline for clean output
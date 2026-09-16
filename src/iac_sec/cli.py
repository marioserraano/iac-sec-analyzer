import typer
import asyncio
from enum import Enum
from typing import Optional
from rich.console import Console
from rich.spinner import Spinner

from iac_sec.parser.hcl_parser import TerraformParser, HclParsingError
from iac_sec.analyzer.engine import SecurityAnalyzer
from iac_sec.reporter.console import ConsoleReporter
from iac_sec.reporter.markdown import MarkdownReporter
from iac_sec.reporter.json_out import JsonReporter

# Create an Enum for our format choices to get automatic CLI validation
class OutputFormat(str, Enum):
    CONSOLE = "console"
    JSON = "json"
    MARKDOWN = "markdown"

# Initialize the Typer app
app = typer.Typer(
    help="AI-powered Infrastructure as Code (IaC) Security Analyzer.",
    add_completion=False,
)

# Send UI logs to stderr so they don't corrupt pure data exports (stdout)
console = Console(stderr=True)

# Main callback function
@app.callback()
def main():
    """Main entrypoint for the CLI."""
    pass

@app.command()
def analyze(
    file_path: str = typer.Argument(..., help="Path to the Terraform (.tf) file to analyze."),
    format: OutputFormat = typer.Option(
        OutputFormat.CONSOLE, 
        "--format", "-f", 
        help="Output format (console, json, markdown)."
    ),
    policy_file: Optional[str] = typer.Option(
        None,
        "--policy", "-p",
        help="Path to a text file containing custom company security policies."
    )
):
    """
    Parses a Terraform file and analyzes it for security vulnerabilities using an LLM.
    """
    
    # We define an internal async function because Typer runs synchronously by default,
    # but our engine's analyze() method is asynchronous.
    async def _run_analysis() -> None:
        try:
            # Phase 0: Load custom policies if provided
            custom_policy_text = None
            if policy_file:
                try:
                    with open(policy_file, "r", encoding="utf-8") as f:
                        custom_policy_text = f.read()
                    console.print(f"[bold cyan]>[/bold cyan] Loaded custom policy from: {policy_file}")
                except FileNotFoundError:
                    console.print(f"[bold red]Error:[/bold red] Policy file '{policy_file}' not found.")
                    raise typer.Exit(code=1)

            # Phase 1: Parse the HCL file
            console.print(f"[bold blue]>[/bold blue] Parsing Terraform file: {file_path}...")
            parsed_data = TerraformParser.parse_file(file_path)
            
            # Phase 2 & 3: Initialize engine and run analysis
            analyzer = SecurityAnalyzer(filename=file_path, custom_policy=custom_policy_text)
            
            with console.status("[bold yellow]Analyzing infrastructure context using local LLM...[/bold yellow]", spinner="dots"):
                # Await the AI's response while showing a loading animation
                report = await analyzer.analyze(parsed_hcl=parsed_data)
                
            # Phase 4: Display the results based on the chosen format strategy
            console.print("[bold green]>[/bold green] Analysis complete!\n")
            
            if format == OutputFormat.JSON:
                print(JsonReporter.generate(report))
            elif format == OutputFormat.MARKDOWN:
                print(MarkdownReporter.generate(report))
            else:
                ConsoleReporter.print_report(report)
            
        except FileNotFoundError as e:
            console.print(f"[bold red]Error:[/bold red] {str(e)}")
            raise typer.Exit(code=1)
        except HclParsingError as e:
            console.print(f"[bold red]Parsing Error:[/bold red] {str(e)}")
            raise typer.Exit(code=1)
        except Exception as e:
            console.print(f"[bold red]Unexpected Error:[/bold red] An error occurred during analysis: {str(e)}")
            raise typer.Exit(code=1)

    # Execute the async function using asyncio's event loop
    asyncio.run(_run_analysis())

if __name__ == "__main__":
    app()
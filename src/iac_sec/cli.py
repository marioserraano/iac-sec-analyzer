import typer
import asyncio
from rich.console import Console
from rich.spinner import Spinner

from iac_sec.parser.hcl_parser import TerraformParser, HclParsingError
from iac_sec.analyzer.engine import SecurityAnalyzer
from iac_sec.reporter.console import ConsoleReporter

# Initialize the Typer app
app = typer.Typer(
    help="AI-powered Infrastructure as Code (IaC) Security Analyzer.",
    add_completion=False,
)
console = Console()

@app.command()
def analyze(
    file_path: str = typer.Argument(..., help="Path to the Terraform (.tf) file to analyze.")
):
    """
    Parses a Terraform file and analyzes it for security vulnerabilities using an LLM.
    """
    
    # We define an internal async function because Typer runs synchronously by default,
    # but our engine's analyze() method is asynchronous.
    async def _run_analysis() -> None:
        try:
            # Phase 1: Parse the HCL file
            console.print(f"[bold blue]>[/bold blue] Parsing Terraform file: {file_path}...")
            parsed_data = TerraformParser.parse_file(file_path)
            
            # Phase 2 & 4: Initialize engine and run analysis
            analyzer = SecurityAnalyzer(filename=file_path)
            
            with console.status("[bold yellow]Analyzing infrastructure context using local LLM...[/bold yellow]", spinner="dots"):
                # Await the AI's response while showing a loading animation
                report = await analyzer.analyze(parsed_hcl=parsed_data)
                
            # Phase 5: Display the results
            console.print("[bold green]>[/bold green] Analysis complete!\n")
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
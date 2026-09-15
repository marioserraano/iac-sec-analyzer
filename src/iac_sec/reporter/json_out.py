from iac_sec.models.schemas import SecurityReport

class JsonReporter:
    """Handles the JSON serialization of the security report."""
    
    @staticmethod
    def generate(report: SecurityReport) -> str:
        """Converts the Pydantic model into a raw JSON string."""
        # Pydantic natively supports JSON export. 
        # We just tell it to indent for readability.
        return report.model_dump_json(indent=2)
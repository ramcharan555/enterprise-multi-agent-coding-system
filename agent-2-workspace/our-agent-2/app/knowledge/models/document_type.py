from enum import Enum


class DocumentType(str, Enum):
    README = "readme"
    API_DOCUMENTATION = "api_documentation"
    ARCHITECTURE = "architecture"
    ADR = "adr"
    DEVELOPER_GUIDELINE = "developer_guideline"
    TECHNICAL_SPECIFICATION = "technical_specification"
    RUNBOOK = "runbook"
    GENERAL = "general"
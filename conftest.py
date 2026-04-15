from src.model import MainframeSnapshot
import pytest

# platform: str = Field(description="he mainframe platform, e.g. IBM z/OS, AS/400, Unisys")
# primary_language: str = Field(description="Primary programming language, e.g. COBOL, PL/I, RPG")
# key_workloads: list[str] = Field(description="List of business functions the system performs")
# integration_type: Literal["batch","online","mixed","api_exposed"] = Field(description="How the system integrates: batch=file/scheduled, online=real-time transactions, mixed=both, api_exposed=has API interface")
# modernization_flags: list[str] = Field(description="Risk or complexity signals relevant to modernization")

@pytest.fixture
def valid_snapshot():
    return MainframeSnapshot(
        platform="IBM z/OS",
        primary_language="COBOL",
        key_workloads=["policy underwriting", "claims processing"],
        integration_type="mixed",
        modernization_flags=["legacy codebase", "high business criticality"]
    )


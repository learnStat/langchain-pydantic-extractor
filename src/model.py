
from pydantic import BaseModel, Field
from typing import Literal


class MainframeSnapshot(BaseModel):
    platform: str = Field(description="The mainframe platform, e.g. IBM z/OS, AS/400, Unisys")
    primary_language: str = Field(description="Primary programming language, e.g. COBOL, PL/I, RPG")
    key_workloads: list[str] = Field(description="List of business functions the system performs")
    integration_type: Literal["batch","online","mixed","api_exposed"] = Field(description="How the system integrates: batch=file/scheduled, online=real-time transactions, mixed=both, api_exposed=has API interface")
    modernization_flags: list[str] = Field(description="Risk or complexity signals relevant to modernization")
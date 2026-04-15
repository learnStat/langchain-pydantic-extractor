import pytest
from src.model import MainframeSnapshot
from pydantic import ValidationError

def test_valid_mainframe_snapshot(valid_snapshot):
    assert isinstance(valid_snapshot, MainframeSnapshot)
    assert valid_snapshot.platform == "IBM z/OS"
    assert valid_snapshot.primary_language == "COBOL"
    assert valid_snapshot.integration_type == "mixed"
    assert isinstance(valid_snapshot.key_workloads, list)
    assert isinstance(valid_snapshot.modernization_flags,list)


def test_invalid_integration_type():
    with pytest.raises(ValidationError):
        MainframeSnapshot(
            platform="IBM z/OS",
            primary_language="COBOL",
            key_workloads=["policy underwriting"],
            integration_type="invalid_type",
            modernization_flags=[]
        )

def test_missing_required_fields():
        with pytest.raises(ValidationError):
             MainframeSnapshot(
                platform="IBM z/OS",
                primary_language="COBOL",
                key_workloads=["policy underwriting"],
                modernization_flags=[]
             )

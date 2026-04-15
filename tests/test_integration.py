from unittest.mock import MagicMock, patch
from src.chain import build_chain
from src.model import MainframeSnapshot
import pytest
from langchain_community.chat_models.fake import FakeListChatModel
import json

fake_response = json.dumps({
    "platform": "IBM z/OS",
    "primary_language": "COBOL",
    "key_workloads": ["policy underwriting", "claims processing"],
    "integration_type": "mixed",
    "modernization_flags": ["legacy codebase", "high business criticality"]
})


def test_chain_invoke_returns_mainframe_snapshot(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "anthropic")  # or "openai" depending on which you want to test
    with patch("src.chain.ChatAnthropic", return_value =FakeListChatModel(responses=[fake_response])):
        chain, provider = build_chain()
        result = chain.invoke({"system_description": "We run COBOL on IBM z/OS"})
    # Assert that the result is a MainframeSnapshot instance and matches the valid snapshot
    assert isinstance(result, MainframeSnapshot)
    assert provider == "anthropic"
    assert result.platform == "IBM z/OS"
    assert result.integration_type == "mixed"

def test_chain_invoke_with_openai_returns_mainframe_snapshot(monkeypatch, valid_snapshot):
    monkeypatch.setenv("LLM_PROVIDER", "openai")

    with patch("src.chain.ChatOpenAI", return_value=FakeListChatModel(responses=[fake_response])):
        chain, provider = build_chain()
        result = chain.invoke({"system_description": "We run COBOL on IBM z/OS"})
    # chain.invoke = MagicMock(return_value=valid_snapshot)  # Mock the invoke method to return the JSON of the valid snapshot
    assert isinstance(result, MainframeSnapshot)
    assert provider == "openai"
    assert result.platform == "IBM z/OS"
    assert result.integration_type == "mixed"
    assert result.primary_language == "COBOL"
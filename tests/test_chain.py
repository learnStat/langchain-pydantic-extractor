import pytest
from src.chain import build_chain
from langchain_core.runnables import RunnableSequence

def test_build_chain_anthropic(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "anthropic")
    chain, provider = build_chain()
    assert provider == "anthropic"
    assert chain is not None
    assert isinstance(chain, RunnableSequence)

def test_build_chain_openai(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER","openai")
    chain, provider = build_chain()
    assert provider == "openai"
    assert chain is not None
    assert isinstance(chain, RunnableSequence)

def test_build_chain_invalid_provider(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "invalid_provider")
    with pytest.raises(ValueError):
        build_chain()
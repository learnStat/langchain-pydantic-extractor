# langchain-pydantic-extractor

A LangChain LCEL chain that extracts structured information from unstructured text using `PydanticOutputParser`. Built as a deliberate refresher and contrast exercise against a prior [PydanticAI project](https://github.com/learnStat/pydantic-ai-mainframe-explainer).

---

## What This Project Does

Takes plain English descriptions of mainframe systems — the kind a client might give in a discovery call — and extracts structured data into a typed Pydantic model using a LangChain LCEL chain.

**Input:** Unstructured paragraph describing a mainframe environment  
**Output:** A typed `MainframeSnapshot` object with five fields

```
platform='IBM z/OS'
primary_language='COBOL'
key_workloads=['Policy underwriting', 'Rating logic processing', 'Batch file generation']
integration_type='batch'
modernization_flags=['File-based handoffs', 'No real-time interface', 'DB2 mainframe dependency']
```

---

## What This Project Teaches

### LangChain LCEL pipe operator
Three components chained with `|`:
```python
prompt | llm | parser
```
Output of each stage feeds the next. Order is strict and intentional — there is no smart routing.

### PydanticOutputParser
LangChain's approach to structured output. The parser converts your Pydantic model into format instructions that are injected into the prompt, asking the LLM to return conforming JSON. Validation happens at parse time — if the LLM doesn't comply, the parser raises an exception.

### `prompt.partial()` for pre-filling variables
`format_instructions` is resolved once inside `build_chain()` and baked into the prompt via `.partial()`. This means `chain.invoke()` only needs the user-supplied variable:
```python
chain.invoke({"system_description": input_text})
```
The caller has zero knowledge of parsers or format instructions.

### Provider switching without code changes
Both Anthropic and OpenAI are supported. Switch providers and models via `.env` — no code changes required:
```
LLM_PROVIDER=anthropic        # or openai
ANTHROPIC_MODEL=claude-haiku-4-5
OPENAI_MODEL=gpt-4o-mini
```

---

## The Key Distinction: LangChain vs PydanticAI

This project was built explicitly to contrast with a prior PydanticAI implementation of similar structured extraction.

| | LangChain PydanticOutputParser | PydanticAI |
|---|---|---|
| **Approach** | Asks the LLM to return the right structure via prompt instructions | Enforces the structure — rejects non-conforming output and retries |
| **Validation** | At parse time, exception if LLM doesn't comply | Built into the framework, automatic retry loop |
| **Pydantic model role** | End of chain, parsing step | Central — the agent is built around it |
| **Output guarantee** | Depends on LLM cooperation | Structural guarantee |

> "LangChain with JSON asks the LLM to try to return the right structure. PydanticAI enforces the structure and rejects anything that doesn't conform."

In practice: running the same three inputs through Anthropic Haiku and GPT-4o-mini produced noticeably different output depth — Haiku returned richer `modernization_flags` with more precise technical language. Same prompt, same schema, meaningfully different results. PydanticAI's enforcement would catch structural non-compliance either way, but output quality variance is a prompt and model concern, not a framework concern.

---

## Project Structure

```
langchain-pydantic-extractor/
├── .env                  # LLM_PROVIDER, model names, API keys
├── requirements.txt
├── main.py               # Entry point — thin orchestrator
├── outputs/              # Saved run results (--save flag)
└── src/
    ├── __init__.py
    ├── model.py          # MainframeSnapshot Pydantic model
    └── chain.py          # Chain assembly, provider switching, env config
```

---

## Setup

```bash
git clone https://github.com/learnStat/langchain-pydantic-extractor
cd langchain-pydantic-extractor
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file:
```
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
LLM_PROVIDER=anthropic
ANTHROPIC_MODEL=claude-haiku-4-5
OPENAI_MODEL=gpt-4o-mini
```

---

## Usage

**Print to terminal:**
```bash
python main.py
```

**Save to file:**
```bash
python main.py --save
```
Output saved to `outputs/{provider}_{timestamp}_output.txt`

---

## The Model

```python
class MainframeSnapshot(BaseModel):
    platform: str
    primary_language: str
    key_workloads: list[str]
    integration_type: Literal["batch", "online", "mixed", "api_exposed"]
    modernization_flags: list[str]
```

`integration_type` is constrained to four valid values via `Literal`. All fields include `Field(description=...)` — these descriptions are consumed by `PydanticOutputParser` to generate the format instructions injected into the prompt, directly affecting output quality.

---

## AI Collaboration

Built with Claude as a collaborative pair programmer. All architecture decisions, design choices, and debugging were made jointly and are understood line by line. Claude is used transparently as a development partner, not a code generator.

import os
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from src.model import MainframeSnapshot
from dotenv import load_dotenv

load_dotenv(override=True )

provider = os.getenv("LLM_PROVIDER", "anthropic")
openai_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
anthropic_model = os.getenv("ANTHROPIC_MODEL", "claude-haiku-4-5")


def build_chain():

    parser = PydanticOutputParser(pydantic_object=MainframeSnapshot)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a mainframe modernization expert. Extract structured information from the system description provided."),
        ("human","{system_description}\n\n{format_instructions}")
    ])
    
    format_instructions = parser.get_format_instructions()
    prompt = prompt.partial(format_instructions=format_instructions)

    if provider == "anthropic":
        llm = ChatAnthropic(model=anthropic_model, temperature=0)
    elif provider == "openai":
        llm = ChatOpenAI(model=openai_model, temperature=0)
    else:
        raise ValueError(f"Unknown provider {provider}")
    
    return (prompt | llm | parser), provider

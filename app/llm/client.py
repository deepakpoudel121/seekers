from langchain_mistralai import ChatMistralAI
from dotenv import load_dotenv
from rich import print
from app.schemas import Llmschema, Matchschema
from langchain_core.prompts import ChatPromptTemplate
from pathlib import Path

load_dotenv()


def load_prompt(name: str) -> str:
    path = Path(__file__).parent /  f"{name}.txt"
    return path.read_text()


extract = load_prompt('prompts/extract_v1')
match = load_prompt('prompts/match_v1')

candidate = load_prompt('candidate_profile')

extractor = ChatPromptTemplate.from_template(extract)
matcher = ChatPromptTemplate.from_template(match)
llm = ChatMistralAI(model = 'mistral-small-latest')
desc_llm = llm.with_structured_output(Llmschema)


match_llm = llm.with_structured_output(Matchschema)

extract_chain = extractor | desc_llm

match_chain = matcher | match_llm

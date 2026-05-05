from langchain_mistralai import ChatMistralAI
from dotenv import load_dotenv
from rich import print
from app.schemas import Llmschema, Matchschema
from langchain_core.prompts import ChatPromptTemplate
from pathlib import Path

load_dotenv()

job_desc = '''🧾 Sample Job Description

Senior Backend Engineer (Python)
📍 Kathmandu, Nepal (Hybrid)

Company: Himalayan Tech Solutions Pvt. Ltd.

Himalayan Tech Solutions is looking for a Senior Backend Engineer to join our growing engineering team. You will be responsible for designing, building, and maintaining scalable backend services that power our fintech platform used by thousands of users across Nepal and South Asia.

Responsibilities
Design and develop RESTful APIs using Python and FastAPI
Build and maintain microservices architecture
Collaborate with frontend engineers, product managers, and DevOps teams
Optimize application performance and ensure high scalability
Write clean, testable, and maintainable code
Requirements
5+ years of experience in backend development
Strong proficiency in Python
Experience with FastAPI or Django
Knowledge of PostgreSQL and Redis
Familiarity with Docker and Kubernetes
Understanding of distributed systems and microservices
Experience with cloud platforms (AWS or GCP)
Nice to Have
Experience in fintech or payment systems
Knowledge of event-driven architecture (Kafka or RabbitMQ)
Compensation
Salary: NPR 150,000 – 250,000 per month
Performance-based bonuses
Health insurance included
Seniority Level
Senior
Employment Type
Full-time'''

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

from pydantic import BaseModel
from typing import Literal

class SalaryRange(BaseModel):
    min_salary: int
    max_salary: int
    currency: str = 'USD'


class Llmschema(BaseModel):
    role: str
    company: str
    required_skills: list[str]
    salary_range: SalaryRange
    seniority_level: Literal['junior', 'mid', 'senior']


class Matchschema(BaseModel):
    match_score: int
    fit_level: Literal['poor', 'fair', 'good', 'strong', 'excellent']
    matching_skills: list[str]
    missing_skills: list[str]
    experience_match: str
    seniority_match: str
    salary_alignment: str
    summary: str


class ApplicationRequest(BaseModel):
    application_content: str

class ApplicationResponse(BaseModel):
    application_id: int
    role:str
    company: str
    required_skills: list[str]
    salary_range: SalaryRange
    seniority_level: Literal['jounior','mid','senior']
from pydantic import BaseModel, ConfigDict
from typing import Literal
from datetime import datetime


class SalaryRange(BaseModel):
    min_salary: int
    max_salary: int
    currency: str = 'USD'


class Llmschema(BaseModel):
    role: str
    company: str
    required_skills: list[str]
    seniority_level: Literal['junior', 'mid', 'senior', 'lead', 'unknown']
    salary_min: int | None
    salary_max: int | None

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
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    role: str
    company: str
    required_skills: list[str] | None
    seniority: str | None
    salary_min: int | None
    salary_max: int | None
    status: str
    match_score: float | None
    match_reasoning: str | None
    created_at: datetime
   


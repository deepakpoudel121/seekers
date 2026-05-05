from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from app.schemas import ApplicationRequest, ApplicationResponse
from app.db import get_db
from app.models import Application
from app.llm import extract_chain, match_chain, candidate
from datetime import datetime
from rich import print
router = APIRouter(prefix='/api/v1/applications')


@router.post('/', response_model= ApplicationResponse)
async def post_application(request: ApplicationRequest, db:AsyncSession = Depends(get_db)):
    try:
        response = await extract_chain.ainvoke({
                'job_description': request.application_content,
            })
        matcher = await match_chain.ainvoke({
            'job_description': request.application_content,
            "candidate_profile": candidate
        })
        print(response, matcher)
        new = Application(
            role = response.role,
            company = response.company,
            required_skills = response.required_skills,
            salary_min = response.salary_range.min_salary,
            salary_max = response.salary_range.max_salary,
            seniority = response.seniority_level,
            raw_jd = request.application_content,
            match_score = matcher.match_score,
            match_reasoning = matcher.summary,
            created_at = datetime.utcnow()
        )
        db.add(new)
        await db.commit()
        await db.refresh(new)
        return new
    except Exception as e:
        return HTTPException(status_code=500, details=str(e))



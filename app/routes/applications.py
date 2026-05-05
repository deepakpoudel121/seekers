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
            salary_min = response.salary_min,
            salary_max = response.salary_max ,
            seniority = response.seniority_level,
            raw_jd = request.application_content,
            match_score = matcher.match_score,
            match_reasoning = matcher.summary
        )
        db.add(new)
        await db.commit()
        await db.refresh(new)
        return new
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/')
async def get_applications(status: str = Query(default=None),
    db: AsyncSession = Depends(get_db)):
    query = select(Application)
    if status:
        query = query.where(Application.status == status)
    result = await db.execute(query)
    applications = result.scalars().all()
    print(applications)
    return {
        'Applications' :[
            {
                "id": app.id,
                'company': app.company,
                'status': app.status
            }
        ] for app in applications
    }

@router.get('/{app_id}')
async def get_applications( app_id: int, db: AsyncSession = Depends(get_db)):
    query = select(Application).where(Application.id == app_id)
    result = await db.execute(query)
    one_application= result.scalars().first()
    return one_application

@router.patch('/{app_id}')
async def change_status(app_id:int,status:str,db:AsyncSession = Depends(get_db)):
    application = await db.execute(select(Application).where(Application.id == app_id))
    one_app = application.scalars().first()
    one_app.status = status
    await db.commit()
    return {"message": "status updated"}



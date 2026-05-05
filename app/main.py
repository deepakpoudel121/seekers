from fastapi import FastAPI
from app.routes import application_router
app = FastAPI()
app.include_router(application_router)
@app.get('/')
def job_seekers():
    return {"messages": "Welcome to Job-Seekes API"}
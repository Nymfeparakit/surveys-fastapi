from fastapi import APIRouter


router = APIRouter(
    prefix='surveys',
)

@router.get("/")
async def get_surveys():
    return {"surveys": "Surveys list"}

@router.get("/{survey_id}")
async def get_survey(survey_id: str):
    return {"survey": "survey"}

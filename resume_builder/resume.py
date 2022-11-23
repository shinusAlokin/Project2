from models import (
    BasicDetails,
    LocationDetails,
    SocialMedia,
    Skills,
    Work,
    Projects,
    Education,
)
from database import SessionLocal
from starlette.responses import JSONResponse
from starlette.exceptions import HTTPException
from utils import *
from sqlalchemy import func
from basic_details import get_basic_util
from schemas import BasicDetailsSchema, SkillsSchema, LocationDetailsSchema
from schemas import EducationSchema, WorkSchema, SocialMediaSchema, ProjectSchema

db = SessionLocal()

# validation utility function
def validate_resume(schema, data, model):
    for i in data:
        schema.from_orm(model(**i))


# Creating new resume
async def create_resume(request):
    new_details = await request.json()
    loc = new_details.pop("location_details")
    social = new_details.pop("social_media")
    work = new_details.pop("work_details")
    edu = new_details.pop("education_details")
    skill = new_details.pop("skills")
    project = new_details.pop("projects")

    new_details = BasicDetails(
        **new_details,
        location_details=[LocationDetails(**i) for i in loc],
        social_media=create_util(SocialMedia, social),
        work_details=create_util(Work, work),
        education_details=create_util(Education, edu),
        skills=create_util(Skills, skill),
        projects=create_util(Projects, project)
    )

    try:
        BasicDetailsSchema.from_orm(new_details)
        validate_resume(SkillsSchema, skill, Skills)
        validate_resume(LocationDetailsSchema, loc, LocationDetails)
        validate_resume(EducationSchema, edu, Education)
        validate_resume(WorkSchema, work, Work)
        validate_resume(ProjectSchema, project, Projects)
        validate_resume(SocialMediaSchema, social, SocialMedia)

        db.add(new_details)
        db.commit()
        db.refresh(new_details)
        new_id = new_details.basic_details_id
        return JSONResponse({"created_id": new_id})

    except Exception as e:
        db.rollback()
        try:
            return JSONResponse({"error_message": e.errors()})
        except:
            return JSONResponse(
                {"error_message": f"You should enter all the required fields correctly"}
            )


# to GET all the data
async def get_all(request):
    fk = request.path_params["fk"]
    basic = get_basic_util(fk)
    skill = get_helper(Skills, fk)
    location = get_helper(LocationDetails, fk)
    work = get_helper(Work, fk)
    education = get_helper(Education, fk)
    project = get_helper(Projects, fk)
    social = get_helper(SocialMedia, fk)
    return JSONResponse(
        {
            "basic": basic,
            "skills": skill,
            "location_details": location,
            "work_details": work,
            "education_details": education,
            "projects": project,
            "social_media": social,
        }
    )


# API to update the resume
async def update_resume(request):
    fk = request.path_params["fk"]
    if request.method == "PUT":
        new_details = await request.json()
        loc = new_details.pop("location_details")
        social = new_details.pop("social_media")
        work = new_details.pop("work_details")
        edu = new_details.pop("education_details")
        skill = new_details.pop("skills")
        project = new_details.pop("projects")
        try:
            BasicDetailsSchema.from_orm(BasicDetails(**new_details))
            validate_resume(SkillsSchema, skill, Skills)
            validate_resume(LocationDetailsSchema, loc, LocationDetails)
            validate_resume(EducationSchema, edu, Education)
            validate_resume(WorkSchema, work, Work)
            validate_resume(ProjectSchema, project, Projects)
            validate_resume(SocialMediaSchema, social, SocialMedia)

            edit_util(BasicDetails, fk, new_details)
            edit_looper_util(skill, Skills, fk)
            edit_looper_util(loc, LocationDetails, fk)
            edit_looper_util(work, Work, fk)
            edit_looper_util(edu, Education, fk)
            edit_looper_util(social, SocialMedia, fk)
            edit_looper_util(project, Projects, fk)
            return JSONResponse({"Success": "Successfully edited"})
        except Exception as e:
            db.rollback()
            return JSONResponse({"error_message": e.errors()})

    basic = get_basic_util(fk)
    skill = get_helper(Skills, fk)
    location = get_helper(LocationDetails, fk)
    work = get_helper(Work, fk)
    education = get_helper(Education, fk)
    project = get_helper(Projects, fk)
    social = get_helper(SocialMedia, fk)
    return JSONResponse(
        {
            "basic": basic,
            "skills": skill,
            "location_details": location,
            "work_details": work,
            "education_details": education,
            "projects": project,
            "social_media": social,
        }
    )


# API for searching content 
async def search(request):
    search = request.path_params["search"]

    if search:
        data = (
            db.query(BasicDetails)
            .filter(
                (func.lower(BasicDetails.name).contains(search.lower()))
                | (BasicDetails.email_address == search)
            )
            .order_by(BasicDetails.date_applied)
            .all()
        )
        content = [
            {
                key: str(value).split(".")[0] if key == "date_applied" else str(value)
                for key, value in result.__dict__.items()
                if key
                in [
                    "name",
                    "email_address",
                    "phone_number",
                    "date_applied",
                    "basic_details_id",
                ]
            }
            for result in data
        ]
    return JSONResponse({"search": content})

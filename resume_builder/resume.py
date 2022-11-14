from models import BasicDetails, LocationDetails, SocialMedia, Skills, Work, Projects, Education
from database import SessionLocal
from starlette.responses import JSONResponse
from starlette.exceptions import HTTPException
from utils import *
from basic_details import get_basic_util
from schemas import BasicDetailsSchema, SkillsSchema, LocationDetailsSchema
from schemas import EducationSchema, WorkSchema, SocialMediaSchema, ProjectSchema

db = SessionLocal()


def validate_resume(schema, data, model):
        for i in data:
            schema.from_orm(model(**i))


async def create_resume(request):
    new_details = await request.json()
    loc = new_details.pop("location_details")
    social = new_details.pop("social_media")
    work = new_details.pop("work_details")
    edu = new_details.pop("education_details")
    skill = new_details.pop("skills")
    project = new_details.pop("projects")
    
    # try:
    #     new_details = BasicDetailsSchema(**new_details)
    # except Exception as e:
    #     return e
    new_details = BasicDetails(**new_details, 
                            location_details=create_util(LocationDetails, loc),
                            social_media=create_util(SocialMedia, social),
                            work_details=create_util(Work, work),
                            education_details=create_util(Education, edu),
                            skills=create_util(Skills, skill),
                            projects=create_util(Projects, project)) 


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
    except Exception as e:
        print(e)
        db.rollback()
        return JSONResponse({'error_message': f'{e}'})
    return JSONResponse({'data': 'new_details'}, status_code=201)
    

async def get_all(request):
    fk = request.path_params["fk"]
    basic = get_basic_util(fk)
    skill = get_helper(Skills, fk)
    location = get_helper(LocationDetails, fk)
    work = get_helper(Work, fk)
    education = get_helper(Education, fk)
    project = get_helper(Projects, fk)
    social = get_helper(SocialMedia, fk)
    return JSONResponse({
        'basic':basic,
        'skills': skill,
        'location_details': location,
        'work_details':work,
        'education_details':education,
        'projects':project,
        'social_media':social
    })


async def update_resume(request):
    fk = request.path_params['fk']
    if request.method == 'PUT':
        new_details = await request.json()
        loc = new_details.pop("location_details")
        social = new_details.pop("social_media")
        work = new_details.pop("work_details")
        edu = new_details.pop("education_details")
        skill = new_details.pop("skills")
        project = new_details.pop("projects")        
        try:

            # BasicDetailsSchema.from_orm(**new_details)
            # BasicDetailsSchema.from_orm(BasicDetails(**new_details))
            validate_resume(SkillsSchema, skill, Skills)
            validate_resume(LocationDetailsSchema, loc, LocationDetails)
            validate_resume(EducationSchema, edu, Education)
            validate_resume(WorkSchema, work, Work)
            validate_resume(ProjectSchema, project, Projects)
            validate_resume(SocialMediaSchema, social, SocialMedia)            
            
            edit_util(BasicDetails, fk, new_details)
            edit_looper_util(skill,Skills,fk)
            edit_looper_util(loc,LocationDetails, fk)
            edit_looper_util(work, Work, fk)
            edit_looper_util(edu, Education, fk)
            edit_looper_util(social, SocialMedia, fk)
            edit_looper_util(project, Projects, fk)
            return JSONResponse({"Success": "Successfully edited"})
        except Exception as e:
            print(e)
            db.rollback()
        return JSONResponse({'edit': 'Update failed'})

    basic = get_basic_util(fk)
    skill = get_helper(Skills, fk)
    location = get_helper(LocationDetails, fk)
    work = get_helper(Work, fk)
    education = get_helper(Education, fk)
    project = get_helper(Projects, fk)
    social = get_helper(SocialMedia, fk)
    return JSONResponse({
        'basic':basic,
        'skills': skill,
        'location_details': location,
        'work_details':work,
        'education_details':education,
        'projects':project,
        'social_media':social
    })


async def search(request):
    search = request.path_params['search']
    
    if search:
        data = db.query(BasicDetails).filter((BasicDetails.name.contains(search)) | (BasicDetails.email_address==search)).order_by(BasicDetails.date_applied).all()
        content = [{key: str(value) for key, value in result.__dict__.items() if key in ['name', 'email_address', 
                    'phone_number', 'date_applied', 'basic_details_id']} 
                for result in data]
    return JSONResponse({'search': content})

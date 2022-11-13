from projects import add_project
from starlette.applications import Starlette
from starlette.routing import Route
from database import SessionLocal, engine
from models import Base
from basic_details import *
from skills import *
from location_details import *
from education import *
from projects import *
from work_exp import *
from social_media import *
from resume import *
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware


Base.metadata.create_all(bind=engine)
db = SessionLocal()



routes = [
        #basic details
        Route('/get_basic/', endpoint=get_basic_details, methods=['GET']),
        Route('/create_basic', endpoint=create_basic_details, methods=['POST']),
        Route('/get_basic/{id:int}', endpoint=get_basic_detail, methods=['GET']),
        Route('/edit/{id:int}', endpoint=edit_basic_detail, methods=['GET','PUT']),
        Route('/delete/{id:int}', endpoint=delete_basic_details, methods=['DELETE']),
        # Route('/get_all/{id:int}', endpoint=get_everything, methods=['GET']),
        
        #skills
        Route('/create_skill/{fk:int}', endpoint=add_skill, methods=['POST']),
        Route('/get_skills/{fk:int}', endpoint=get_skills, methods=['GET']),
        Route('/edit_skills/{fk:int}/skill/{pk:int}', endpoint=update_skill, methods=['GET', 'PUT']),
        Route('/delete_skills/{fk:int}/skill/{pk:int}', endpoint=delete_skill, methods=['GET', 'DELETE']),
        # Route('/get_basic_skills/{pk:int}/skill', endpoint=get_skill_basic, methods=['GET']),

        #education
        Route('/create_education/{fk:int}', endpoint=add_education, methods=['POST']),
        Route('/get_education/{fk:int}', endpoint=get_education, methods=['GET']),
        Route('/edit_education/{fk:int}/edu/{pk:int}', endpoint=update_education, methods=['GET', 'PUT']),
        Route('/delete_education/{fk:int}/edu/{pk:int}', endpoint=delete_education, methods=['GET', 'DELETE']),

        #location
        Route('/create_location/{fk:int}', endpoint=add_location, methods=['POST']),
        Route('/get_location/{fk:int}', endpoint=get_location, methods=['GET']),
        Route('/edit_location/{fk:int}/location/{pk:int}', endpoint=update_location, methods=['GET', 'PUT']),
        Route('/delete_location/{fk:int}/location/{pk:int}', endpoint=delete_location, methods=['GET', 'DELETE']),

        #projects
        Route('/create_project/{fk:int}', endpoint=add_project, methods=['POST']),
        Route('/get_project/{fk:int}', endpoint=get_project, methods=['GET']),
        Route('/edit_project/{fk:int}/project/{pk:int}', endpoint=update_project, methods=['GET', 'PUT']),
        Route('/delete_project/{fk:int}/project/{pk:int}', endpoint=delete_project, methods=['GET', 'DELETE']),   

        #work
        Route('/create_work/{fk:int}', endpoint=add_work, methods=['POST']),
        Route('/get_work/{fk:int}', endpoint=get_work, methods=['GET']),
        Route('/edit_work/{fk:int}/work/{pk:int}', endpoint=update_work, methods=['GET', 'PUT']),
        Route('/delete_work/{fk:int}/work/{pk:int}', endpoint=delete_work, methods=['GET', 'DELETE']),     

        #social media
        Route('/create_social_media/{fk:int}', endpoint=add_social_media, methods=['POST']),
        Route('/get_social_media/{fk:int}', endpoint=get_social_media, methods=['GET']),
        Route('/edit_social_media/{fk:int}/social_media/{pk:int}', endpoint=update_social_media, methods=['GET', 'PUT']),
        Route('/delete_social_media/{fk:int}/social_media/{pk:int}', endpoint=delete_social_media, methods=['GET', 'DELETE']),           

        # resume
        Route('/api/new/resume', endpoint=create_resume, methods=['POST']),
        Route('/api/resume/{fk:int}', endpoint=get_all, methods=['GET']),
        Route('/api/update/resume/{fk:int}', endpoint=update_resume, methods=['GET', 'PUT']),

        # search
        Route('/api/search/{search:str}', endpoint=search, methods=['GET'])

]

middleware = [
    Middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'])
]

app = Starlette(debug=True, routes=routes, middleware=middleware)



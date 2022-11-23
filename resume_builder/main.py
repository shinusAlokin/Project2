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
    # basic details
    Route("/get_basic/", endpoint=get_basic_details, methods=["GET"]),
    Route("/create_basic", endpoint=create_basic_details, methods=["POST"]),
    Route("/get_basic/{id:int}", endpoint=get_basic_detail, methods=["GET"]),
    Route("/edit/{id:int}", endpoint=edit_basic_detail, methods=["GET", "PUT"]),
    Route("/delete/{id:int}", endpoint=delete_basic_details, methods=["DELETE"]),
   
    # skills
    Route(
        "/delete_skills/{fk:int}/skill/{pk:int}",
        endpoint=delete_skill,
        methods=["GET", "DELETE"],
    ),

    # education
    Route(
        "/delete_education/{fk:int}/edu/{pk:int}",
        endpoint=delete_education,
        methods=["GET", "DELETE"],
    ),
    # location
    Route(
        "/delete_location/{fk:int}/location/{pk:int}",
        endpoint=delete_location,
        methods=["GET", "DELETE"],
    ),
    # projects
    Route(
        "/delete_project/{fk:int}/project/{pk:int}",
        endpoint=delete_project,
        methods=["GET", "DELETE"],
    ),
    # work
    Route(
        "/delete_work/{fk:int}/work/{pk:int}",
        endpoint=delete_work,
        methods=["GET", "DELETE"],
    ),
    # social media
    Route(
        "/delete_social_media/{fk:int}/social_media/{pk:int}",
        endpoint=delete_social_media,
        methods=["GET", "DELETE"],
    ),
    # resume
    Route("/api/new/resume", endpoint=create_resume, methods=["POST"]),
    Route("/api/resume/{fk:int}", endpoint=get_all, methods=["GET"]),
    Route(
        "/api/update/resume/{fk:int}", endpoint=update_resume, methods=["GET", "PUT"]
    ),
    # search
    Route("/api/search/{search:str}", endpoint=search, methods=["GET"]),
]

middleware = [Middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"])]

app = Starlette(debug=True, routes=routes, middleware=middleware)

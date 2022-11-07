from starlette.responses import JSONResponse
from models import Projects
from database import SessionLocal
from utils import *

db = SessionLocal()

# def create_helper(request, class_name, results):
#     results["basic_details_id"] = request.path_params['fk']
#     new_entity = class_name(**results)
#     db.add(new_entity)
#     db.commit()
#     db.refresh(new_entity)

async def add_project(request):
    new_project = await request.json()
    create_helper(request, Projects, new_project)
    return JSONResponse({'created': 'project added'}, status_code=200)

async def get_project(request):
    id = request.path_params['fk']
    content = get_helper(Projects, id)
    return JSONResponse({'Projects': content})

async def update_project(request):
    fk = request.path_params['fk']
    pk = request.path_params['pk']
    if request.method == "PUT":
        updated = await request.json()
        edit_helper(Projects, pk, fk, updated)
        return JSONResponse({'message': 'Successfully edited'}, status_code=200)
    content = get_helper(Projects, fk)
    return JSONResponse({'Projects': content})

async def delete_project(request):
    pk = request.path_params["pk"]
    fk = request.path_params["fk"]
    if request.method == 'DELETE':
        delete_helper(Projects, pk, fk)
        return JSONResponse({'deleted': 'deleted Projects'}, status_code=204)
    content = get_helper(Projects, fk)
    return JSONResponse({'Projects': content})


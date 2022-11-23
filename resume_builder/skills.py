from starlette.responses import JSONResponse

from models import Skills
from utils import *


async def add_skill(request):
    new_skill = await request.json()
    create_helper(request, Skills, new_skill)
    return JSONResponse({"created": "skills added"}, status_code=201)


async def get_skills(request):
    id = request.path_params["fk"]
    content = get_helper(Skills, id)
    return JSONResponse({"skills": content})


async def update_skill(request):
    fk = request.path_params["fk"]
    pk = request.path_params["pk"]
    if request.method == "PUT":
        updated = await request.json()
        edit_helper(Skills, pk, fk, updated)
        return JSONResponse({"message": "Successfully edited"}, status_code=200)
    content = get_helper(Skills, fk)
    return JSONResponse({"skills": content})


async def delete_skill(request):
    pk = request.path_params["pk"]
    fk = request.path_params["fk"]
    if request.method == "DELETE":
        delete_helper(Skills, pk, fk)
        return JSONResponse({"deleted": "deleted skills"}, status_code=204)
    content = get_helper(Skills, fk)
    return JSONResponse({"skills": content})


async def get_skill_basic(request):
    pk = request.path_params["pk"]
    content = get_relation(Skills, pk)
    print(content)
    return JSONResponse({"basic details with skill": content})

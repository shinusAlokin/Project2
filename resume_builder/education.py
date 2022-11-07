from starlette.responses import JSONResponse
from models import Education
from database import SessionLocal
from utils import *

db = SessionLocal()


async def add_education(request):
    new_education = await request.json()
    create_helper(request, Education, new_education)
    return JSONResponse({'created': 'education added'}, status_code=200)

async def get_education(request):
    id = request.path_params['fk']
    content = get_helper(Education, id)
    return JSONResponse({'Education': content})

async def update_education(request):
    fk = request.path_params['fk']
    pk = request.path_params['pk']
    if request.method == "PUT":
        updated = await request.json()
        edit_helper(Education, pk, fk, updated)
        return JSONResponse({'message': 'Successfully edited'}, status_code=200)
    content = get_helper(Education, fk)
    return JSONResponse({'Education': content})

async def delete_education(request):
    pk = request.path_params["pk"]
    fk = request.path_params["fk"]
    if request.method == 'DELETE':
        delete_helper(Education, pk, fk)
        return JSONResponse({'deleted': 'deleted Education'}, status_code=204)
    content = get_helper(Education, fk)
    return JSONResponse({'Education': content})


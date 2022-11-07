from database import SessionLocal
from starlette.responses import JSONResponse
from models import LocationDetails
from database import SessionLocal
from utils import *

db = SessionLocal()


async def add_location(request):
    new_location = await request.json()
    create_helper(request, LocationDetails, new_location)
    return JSONResponse({"created": "location created"}, status_code=201)

async def get_location(request):
    id = request.path_params['fk']
    content = get_helper(LocationDetails, id)
    return JSONResponse({'LocationDetails': content})

async def update_location(request):
    fk = request.path_params['fk']
    pk = request.path_params['pk']
    if request.method == "PUT":
        updated = await request.json()
        edit_helper(LocationDetails, pk, fk, updated)
        return JSONResponse({'message': 'Successfully edited'}, status_code=200)
    content = get_helper(LocationDetails, fk)
    return JSONResponse({'LocationDetails': content})

async def delete_location(request):
    pk = request.path_params["pk"]
    fk = request.path_params["fk"]
    if request.method == 'DELETE':
        delete_helper(LocationDetails, pk, fk)
        return JSONResponse({'deleted': 'deleted LocationDetails'}, status_code=204)
    content = get_helper(LocationDetails, fk)
    return JSONResponse({'LocationDetails': content})


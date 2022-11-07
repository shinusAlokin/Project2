from starlette.responses import JSONResponse
from models import Work
from database import SessionLocal
from utils import *

db = SessionLocal()

# def create_helper(request, class_name, results):
#     results["basic_details_id"] = request.path_params['fk']
#     new_entity = class_name(**results)
#     db.add(new_entity)
#     db.commit()
#     db.refresh(new_entity)

async def add_work(request):
    new_work = await request.json()
    create_helper(request, Work, new_work)
    return JSONResponse({'created': 'work added'}, status_code=201)

async def get_work(request):
    id = request.path_params['fk']
    content = get_helper(Work, id)
    print(content)
    return JSONResponse({'Work': content})

async def update_work(request):
    fk = request.path_params['fk']
    pk = request.path_params['pk']
    if request.method == "PUT":
        updated = await request.json()
        edit_helper(Work, pk, fk, updated)
        return JSONResponse({'message': 'Successfully edited'}, status_code=200)
    content = get_helper(Work, fk)
    return JSONResponse({'Work': content})

async def delete_work(request):
    pk = request.path_params["pk"]
    fk = request.path_params["fk"]
    if request.method == 'DELETE':
        delete_helper(Work, pk, fk)
        return JSONResponse({'deleted': 'deleted Work'}, status_code=204)
    content = get_helper(Work, fk)
    return JSONResponse({'Work': content})


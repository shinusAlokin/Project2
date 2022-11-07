from starlette.responses import JSONResponse
from models import SocialMedia
from database import SessionLocal
from utils import *

db = SessionLocal()

# def create_helper(request, class_name, results):
#     results["basic_details_id"] = request.path_params['fk']
#     new_entity = class_name(**results)
#     db.add(new_entity)
#     db.commit()
#     db.refresh(new_entity)

async def add_social_media(request):
    new_social_media = await request.json()
    create_helper(request, SocialMedia, new_social_media)
    return JSONResponse({'created':'added social media'}, status_code=200)


async def get_social_media(request):
    id = request.path_params['fk']
    content = get_helper(SocialMedia, id)
    return JSONResponse({'SocialMedia': content})

async def update_social_media(request):
    fk = request.path_params['fk']
    pk = request.path_params['pk']
    if request.method == "PUT":
        updated = await request.json()
        edit_helper(SocialMedia, pk, fk, updated)
        return JSONResponse({'message': 'Successfully edited'}, status_code=200)
    content = get_helper(SocialMedia, fk)
    return JSONResponse({'SocialMedia': content})

async def delete_social_media(request):
    pk = request.path_params["pk"]
    fk = request.path_params["fk"]
    if request.method == 'DELETE':
        delete_helper(SocialMedia, pk, fk)
        return JSONResponse({'deleted': 'deleted SocialMedia'}, status_code=204)
    content = get_helper(SocialMedia, fk)
    return JSONResponse({'SocialMedia': content})


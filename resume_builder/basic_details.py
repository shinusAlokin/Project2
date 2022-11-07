from starlette.responses import JSONResponse
from starlette.exceptions import HTTPException
from sqlalchemy.orm.exc import UnmappedInstanceError
from models import BasicDetails, LocationDetails, SocialMedia, Skills, Work, Projects, Education
from sqlalchemy import inspect
from database import SessionLocal

db = SessionLocal()


def get_basic_util(fk, name=None):
    id = fk
    results = db.query(BasicDetails).filter(BasicDetails.basic_details_id == id).first()
    if not results:
        raise HTTPException(status_code=404, detail="Invalid id")
    content = {}
    for key, value in results.__dict__.items():
        if key=='date_applied':
            content[key] = str(value).split(" ")[0]
        elif key == '_sa_instance_state':
            continue
        else:
            content[key] = value
    return content

async def create_basic_details(request):
    new_details = await request.json()
    new_details = BasicDetails(**new_details)
    db.add(new_details)
    db.commit()
    db.refresh(new_details)
    return JSONResponse({'data': 'created'}, status_code=201)

async def get_basic_details(request):
    results = db.query(BasicDetails).all() 
    content = [{key: value for key, value in result.__dict__.items() if key != '_sa_instance_state'} 
                for result in results]
    content = [{key: str(value).split(" ")[0] if key=='date_applied' else value for key, value in cont.items()} 
                for cont in content]
    return JSONResponse({'content': content}, status_code=200)

async def get_basic_detail(request):
    id = request.path_params["id"]
    results = db.query(BasicDetails).filter(BasicDetails.basic_details_id == id).first()
    if not results:
        raise HTTPException(status_code=404, detail="Invalid id")
    content = {}
    for key, value in results.__dict__.items():
        if key=='date_applied':
            content[key] = str(value).split(" ")[0]
        elif key == '_sa_instance_state':
            continue
        else:
            content[key] = value
    return JSONResponse({'data': content})


async def edit_basic_detail(request):
    print("calling")
    id = request.path_params["id"]
    results_query = db.query(BasicDetails).filter(BasicDetails.basic_details_id == id)
    if not results_query.first():
        raise HTTPException(status_code=404, detail="Invalid id")
    if request.method == 'PUT':
        try:
            updated_details = await request.json()
            results_query.update(updated_details, synchronize_session=False)
            db.commit()
        except Exception as e:
            print(e)
    return JSONResponse({'message': 'Successfully edited'}, status_code=200)


async def delete_basic_details(request):
    id = request.path_params["id"]
    results = db.query(BasicDetails).filter(BasicDetails.basic_details_id == id)
    if not results.first():
        raise HTTPException(status_code=404, detail="Doesn't exist")
    results.delete()
    db.commit()
    return JSONResponse({"message": "successfully deleted"}, status_code=204)


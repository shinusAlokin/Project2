from database import SessionLocal
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse
from schemas import *
# from main import create_helper, get_helper

db = SessionLocal()


def create_helper(request, class_name, results):
    results["basic_details_id"] = request.path_params['fk']
    new_entity = class_name(**results)
    db.add(new_entity)
    db.commit()
    db.refresh(new_entity)

def get_helper(class_name, id):
    results = db.query(class_name).filter(class_name.basic_details_id == id).all()
    content = [{key: value for key, value in result.__dict__.items() if key != '_sa_instance_state'} 
                for result in results]
    content = [{key: str(value) if type(value) not in [str, int] else value for key, value in cont.items() } 
                for cont in content]
    return content

def get_relation(class_name, pk):
    results = db.query(class_name).filter(class_name.basic_details_id==pk).all()
    # results = [result for res in results for result in res]
    content = [{key: value for key, value in result.__dict__.items() if type(value) in [int, str]} 
            for result in results]
    return content

def edit_helper(class_name, pk, fk, updated_value):
    result_query = db.query(class_name).filter((class_name.basic_details_id == fk) & (class_name.id == pk))
    if not result_query.first():
        raise HTTPException(status_code=404, detail="Invalid id")
    result_query.update(updated_value, synchronize_session=False)
    db.commit()


def delete_helper(class_name, pk, fk):
    results = db.query(class_name).filter((class_name.basic_details_id == fk) & (class_name.id == pk))
    if not results.first():
        raise HTTPException(status_code=404, detail="Doesn't exist")
    results.delete()
    db.commit()
    print(results)

def create_util(class_name, data):
    resume_data = [class_name(**i) for i in data]
    return resume_data

def edit_util(class_name, pk, updated_value):
    result_query = db.query(class_name).filter(class_name.basic_details_id == pk)
    if not result_query.first():
        raise HTTPException(status_code=404, detail="Invalid id")
    result_query.update(updated_value, synchronize_session=False)
    db.commit()
    print(result_query)

def edit_looper_util(entity, class_name, fk):
    for ent in entity:
        if not ent.get('id', ''):
            ent['basic_details_id'] = fk
            new_val=class_name(**ent)
            db.add(new_val)
            db.commit()
            db.refresh(new_val)
        else:
            edit_helper(class_name, ent['id'], fk, ent)

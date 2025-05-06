from flask import abort, make_response
from ..db import db

def validate_model(cls, id):
    try:
        id = int(id)
    except:
        response = {"message": f"{cls.__name__} {id} is invalid"}
        abort(make_response(response, 400))

    # check if book_id exists if it is valid type
    query = db.select(cls).where(cls.id == id)
    model = db.session.scalar(query)

    if not model: 
        response = {"message": f"{cls.__name__} {id} not found"}
        abort(make_response(response, 404))
    
    return model

def create_model(cls, model_data):
    try:
        new_model = cls.from_dict(model_data)

    except KeyError as error:
        response = {"message": f"Invalid request: missing {error.args[0]}"}
        abort(make_response(response, 400))
    
    return new_model
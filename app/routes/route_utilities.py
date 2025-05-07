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
    
    db.session.add(new_model)
    db.session.commit()

    #return new_model.to_dict(), 201
    return make_response(new_model.to_dict(), 201)

def get_models_with_filters(cls, filters=None):
    query = db.select(cls)
    
    if filters:
        for filter, value in filters.items():
            if hasattr(cls, filter):
                query = query.where(getattr(cls, filter).ilike(f"%{value}%"))

    query = query.order_by(cls.id)
    models = db.session.scalars(query)

    return [model.to_dict() for model in models]
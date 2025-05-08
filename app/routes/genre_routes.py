from flask import Blueprint, request
from .route_utilities import create_model, get_models_with_filters, validate_model
from ..models.genre import Genre

bp = Blueprint("genre", __name__, url_prefix="/genres")

@bp.post("")
def create_genre():
    request_body = request.get_json()

    return create_model(Genre, request_body)

@bp.get("")
def get_all_genres():
    return get_models_with_filters(Genre, request.args)

@bp.get("/<id>")
def get_one_genre(id):
    genre = validate_model(Genre, id)

    return genre.to_dict()
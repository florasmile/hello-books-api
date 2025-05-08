from flask import Blueprint, request, Response
from .route_utilities import create_model, get_models_with_filters, validate_model
from ..models.genre import Genre
from ..models.book import Book
from ..db import db

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

# nested routes
@bp.post("/<genre_id>/books")
def create_book_with_genre(genre_id):
    genre = validate_model(Genre, genre_id)
    request_body = request.get_json()
    request_body["genres"] = [genre]

    return create_model(Book, request_body)

@bp.get("/<genre_id>/books")
def get_books_with_genre(genre_id):
    genre = validate_model(Genre, genre_id)
    response = [book.to_dict() for book in genre.books]
    return response

@bp.put("/<genre_id>/books/<book_id>")
def update_book_with_genre(genre_id, book_id):
    genre = validate_model(Genre, genre_id)
    book = validate_model(Book, book_id)
    data = {"genres": [genre]}
    book.update_from_dict(data)

    db.session.commit()

    return Response(status=204, mimetype='application/json')

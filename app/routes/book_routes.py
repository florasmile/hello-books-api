from flask import Blueprint, abort, make_response, request, Response
from app.models.book import Book
from app.models.author import Author
from ..db import db
from .route_utilities import validate_model, create_model, get_models_with_filters

bp = Blueprint("books_bp", __name__, url_prefix="/books")

@bp.post("")
def create_book():
    request_body = request.get_json()

    return create_model(Book, request_body)

@bp.get("")
def get_all_books():
    return get_models_with_filters(Book, request.args)

# define endpoints for getting a record of one book by id
@bp.get("/<book_id>")
def get_one_book(book_id):
    book = validate_model(Book, book_id)

    return book.to_dict()


@bp.put("/<book_id>")
def update_book(book_id):
    book = validate_model(Book, book_id)
    request_body = request.get_json()

    book.title = request_body["title"]
    book.description = request_body["description"]
    # assume two cases: no author info or provided an author id; 
    # case 1: no author info
    # case 2:provide author id
        #validate author id
            # case 2a: if exists, update author name
            # case 2b: if not exist, return error message
    # author_id = request_body.get("author_id")
    # if author_id:
    #     author = validate_model(Author, author_id)
    #     #update book author info
    #     book.author_id = author.id
    #     book.author = author.name
    
    db.session.commit()

    return Response(status=204, mimetype='application/json')

@bp.delete("/<book_id>")
def delete_book(book_id):
    book = validate_model(Book, book_id)

    db.session.delete(book)
    db.session.commit()

    return Response(status=204, mimetype="application/json")
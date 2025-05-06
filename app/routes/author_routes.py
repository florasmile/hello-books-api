from flask import Blueprint, request, abort, make_response
from ..db import db
from ..models.author import Author
from ..models.book import Book
from .route_utilities import validate_model, create_model

bp = Blueprint("authors_bp", __name__, url_prefix="/authors")


@bp.get("")
def get_all_authors():
    query = db.select(Author)
    name_param = request.args.get("name")

    if name_param:
        query = query.where(Author.name.ilike(f"%{name_param}%"))

    query = query.order_by(Author.id)
    authors = db.session.scalars(query)

    return [author.to_dict() for author in authors]

@bp.post("")
def create_author():
    request_body = request.get_json()

    new_author = create_model(Author, request_body)

    db.session.add(new_author)
    db.session.commit()

    return new_author.to_dict(), 201

@bp.post("/<author_id>/books")
def create_book_with_author(author_id):
    author = validate_model(Author, author_id)

    request_body = request.get_json()
    request_body["author_id"] = author.id

    new_book = create_model(Book, request_body)
      
    author.books.append(new_book)
    
    db.session.add(new_book)
    db.session.commit()

    return make_response(new_book.to_dict(), 201)

@bp.get("/<author_id>/books")
def get_all_books_with_author(author_id):
    author = validate_model(Author, author_id)

    #return a list of books (as dictionaries)
    response = [book.to_dict() for book in author.books]
    return response
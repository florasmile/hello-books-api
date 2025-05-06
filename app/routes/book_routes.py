from flask import Blueprint, abort, make_response, request, Response
from app.models.book import Book
from app.models.author import Author
from ..db import db
from .route_utilities import validate_model, create_model

bp = Blueprint("books_bp", __name__, url_prefix="/books")

@bp.post("")
def create_book():
    request_body = request.get_json()

    new_book = create_model(Book, request_body)

    db.session.add(new_book)
    db.session.commit()

    return new_book.to_dict(), 201
@bp.get("")
def get_all_books():
    query = db.select(Book)
    
    title_param = request.args.get("title")

    if title_param:
        query = query.where(Book.title.ilike(f"%{title_param}%"))

    description_param = request.args.get("description")
    if description_param:
        query = query.where(Book.description.ilike(f"%{description_param}%"))

    query = query.order_by(Book.id)

    books = db.session.scalars(query)
    books_response = []
    for book in books:
        books_response.append(
            book.to_dict()
        )
    return books_response

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
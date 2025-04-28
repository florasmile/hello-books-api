from flask import Blueprint, abort, make_response, request, Response
from app.models.book import Book
from ..db import db


books_bp = Blueprint("books_bp", __name__, url_prefix="/books")

@books_bp.post("")
def create_book():
    request_body = request.get_json()
    title = request_body["title"]
    description = request_body["description"]

    new_book = Book(title=title, description=description)
    db.session.add(new_book)
    db.session.commit()

    response = {
        "id": new_book.id,
        "title": new_book.title,
        "description": new_book.description,
    }
    return response, 201
@books_bp.get("/")
def get_all_books():
    query = db.select(Book)
    
    title_param = request.args.get("title")

    description_param = request.args.get("description")
    if title_param:
        query = query.where(Book.title.ilike(f"%{title_param}%"))

    if description_param:
        query = query.where(Book.description.ilike(f"%{description_param}%"))

    query = query.order_by(Book.id)

    books = db.session.scalars(query)
    books_response = []
    for book in books:
        books_response.append(
            {
                "id": book.id,
                "title": book.title,
                "description": book.description
            }
        )
    return books_response

# define endpoints for getting a record of one book by id
@books_bp.get("/<book_id>")
def get_one_book(book_id):
    book = validate_one_book(book_id)

    return {
        "id": book.id,
        "title": book.title,
        "description": book.description
    }


# helper: validate the book_id: check id is in correct data type and if it exists in the database;
def validate_one_book(book_id):
    try:
        book_id = int(book_id)
    except:
        response = {"message": f"Book_id {book_id} is invalid"}
        abort(make_response(response, 400))

    # check if book_id exists if it is valid type
    query = db.select(Book).where(Book.id == book_id)
    book = db.session.scalar(query)

    if not book: 
        response = {"message": f"book {book_id} not found"}
        abort(make_response(response, 404))
    
    return book

@books_bp.put("/<book_id>")
def update_book(book_id):
    book = validate_one_book(book_id)
    request_body = request.get_json()

    book.title = request_body["title"]
    book.description = request_body["description"]
    db.session.commit()

    return Response(status=204, mimetype='application/json')

@books_bp.delete("/<book_id>")
def delete_book(book_id):
    book = validate_one_book(book_id)

    db.session.delete(book)
    db.session.commit()

    return Response(status=204, mimetype="application/json")
from flask import Blueprint
from app.models.book import books

books_bp = Blueprint("books_bp", __name__, url_prefix="/books")

@books_bp.get("")
def get_all_books():
  books_list = []
  # loop through books list
  # create a dict for each book 
  # append it to a list
  for book in books:
    books_list.append(
      {
        "id": book.id,
        "title": book.title,
        "description": book.description
      }
    )
  return books_list

@books_bp.get("/<book_id>")
def get_one_book(book_id):
  book_id = int(book_id)
  for book in books:
    if book.id == book_id:
      return {
        "id": book.id,
        "title": book.title,
        "description": book.description
      }
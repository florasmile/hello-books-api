from flask import Blueprint
from app.models.book import books

books_bp = Blueprint("books_bp", __name__, url_prefix="/books")

@books_bp.get("")
def get_all_books():
  books_response = []
  # loop through books list
  # create a dict for each book 
  # append it to a list
  for book in books:
    books_response.append(
      {
        "id": book.id,
        "title": book.title,
        "description": book.description
      }
    )
  return books_response

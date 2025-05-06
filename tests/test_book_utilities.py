import pytest
from app.models.book import Book
from app.routes.route_utilities import validate_model

def test_validate_book(two_saved_books):
    # Act
    # Add `Book` argument to `validate_book` invocation
    result_book = validate_model(Book, 1)

    # Assert
    assert result_book.id == 1
    assert result_book.title == "Ocean Book"
    assert result_book.description == "watr 4evr"
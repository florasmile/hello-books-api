from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from .book import Book

class Author(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    books: Mapped[list["Book"]] = relationship(back_populates="author")

    @classmethod
    def from_dict(cls, author_data):
        name = author_data["name"]
        new_author = cls(name=name)
        books = author_data.get("books")
        if books:
            new_author.books = books
        
        return new_author
    
    def to_dict(self):
        author_to_dict = {
            "id": self.id,
            "name": self.name,
        }
        if self.books: 
            author_to_dict["books"] = self.books
        return author_to_dict

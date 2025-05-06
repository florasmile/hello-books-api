from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import Optional
from ..db import db

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .author import Author

class Book(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    author_id: Mapped[Optional[int]] = mapped_column(ForeignKey("author.id"))
    author: Mapped[Optional["Author"]] = relationship(back_populates="books")


    @classmethod
    def from_dict(cls, book_data):
        title = book_data["title"]
        description = book_data["description"]

        return cls(title=title, description=description)
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description
        }

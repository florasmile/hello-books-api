from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import Optional
from ..db import db


class Book(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    author_id: Mapped[Optional[int]] = mapped_column(ForeignKey("author.id"))
    author: Mapped[Optional["Author"]] = relationship(back_populates="books")

    @classmethod
    def from_dict(cls, data):
        return cls(
            title=data["title"], description=data["description"], author_id=data.get("author_id")
        )
    
    def to_dict(self):
        book_to_dict = {
            "id": self.id,
            "title": self.title,
            "description": self.description
        }
        if self.author_id:
            book_to_dict["author_id"] = self.author_id
        return book_to_dict

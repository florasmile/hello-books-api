from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import Optional
from ..db import db


class Book(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]

    author_id: Mapped[Optional[int]] = mapped_column(ForeignKey("author.id"))
    author: Mapped["Author"] = relationship(back_populates="books")

    genres: Mapped[list["Genre"]] = relationship(secondary="book_genre", back_populates="books")

    @classmethod
    def from_dict(cls, data):
        return cls(
            title=data["title"], description=data["description"], author_id=data.get("author_id"),
            genres=data.get("genres", [])
        )

    
    def to_dict(self):
        book_to_dict = {
            "id": self.id,
            "title": self.title,
            "description": self.description
        }
        if self.author_id:
            book_to_dict["author_id"] = self.author_id
        if self.genres:
            book_to_dict["genres"] = [genre.name for genre in self.genres]
        return book_to_dict
    
    def update_from_dict(self, data):
        for key, value in data.items():
            if key == "genres":
                self.genres.extend(value)
            elif hasattr(self, key):
                self.key = value
   
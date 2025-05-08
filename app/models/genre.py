from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db

class Genre(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    

    @classmethod
    def from_dict(cls, data):
        return cls(name=data["name"])
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }
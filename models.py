import os
from dotenv import load_dotenv
from sqlalchemy import ForeignKey, create_engine
from sqlalchemy.orm import (DeclarativeBase,
                            Mapped,
                            mapped_column,
                            sessionmaker)


load_dotenv()
DB_PATH = os.getenv("DB_PATH")

engine = create_engine(DB_PATH, echo=False, connect_args={'check_same_thread': False})
session = sessionmaker(engine)

class Base(DeclarativeBase):
    pass


class Films(Base):
    __tablename__ = 'films'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    year: Mapped[int]
    rating: Mapped[float]

    def __repr__(self):
        return f"id={self.id}, name={self.name}, year={self.year}, rating={self.rating}"


class Tag(Base):
    __tablename__ = 'tag'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    def __repr__(self):
        return f"id={self.id}, name={self.name}"


class ConnectionTable(Base):
    __tablename__ = 'connectiontable'

    id: Mapped[int] = mapped_column(primary_key=True)

    film_id: Mapped[int] = mapped_column(
        ForeignKey("films.id", ondelete="CASCADE")
    )
    tag_id: Mapped[int] = mapped_column(
        ForeignKey("tag.id", ondelete="CASCADE")
    )

    def __repr__(self):
        return f"id={self.id}, film_id={self.film_id}, tag_id={self.tag_id}"


def create_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


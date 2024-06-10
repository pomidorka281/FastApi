from pydantic import BaseModel


class PFilms(BaseModel):
    name: str
    year: str
    rating: float


class Films(PFilms):
    id: int


class PTag(BaseModel):
    name: str


class Tag(PTag):
    id: int

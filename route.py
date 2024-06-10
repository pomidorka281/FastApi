import uvicorn
import schemas
import crud

from fastapi import FastAPI

app = FastAPI()
Film = schemas.Films
Tag = schemas.Tag

crud = crud.CRUD()


@app.post('/film/')
def create_film(film: dict):
    return crud.create_film(film=dict(film))


@app.get('/film/')
def get_films(year: int = 2024, tags=None):
    if tags is None:
        tags = ["A", "B", "C"]
    return crud.get_films(year=year, tags=tags)


@app.get('/film/{film_id}')
def get_film(film_id: int):
    return crud.get_film(film_id=film_id)


@app.put('/film/{film_id}')
def update_film(film_id: int, new_film: dict):
    return crud.update_comment(film_id=film_id, new_film=new_film)


@app.delete('/film/{film_id}')
def delete_film(film_id: int):
    return crud.delete_film(film_id=film_id)


if __name__ == 'main':
    uvicorn.run(app, host="127.0.0.1", port=8000)


# now it is my new repo!
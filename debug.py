import models
import route

models.create_db()

film = {"name": "string", "year": 2024, "rating": 10,
                "tags":['A', 'B', 'C']}
print(f'Создали film:\n{route.create_film(film=film)}\n')

print(f'get_film:\n{route.get_film(1)}\n')
tag = ['A', 'B', 'C']
print(f'get_films:\n{route.get_films(year=2024, tags=tag)}\n')

film = {"name": "qwer", "year": 2023, "rating": 8.9, "tags":['3', '2', 'r']}
print(f'update_film:\n{route.update_film(1, film)}\n')

film = {"name": "string", "year": 2024, "rating": 10,
                "tags":['A', 'B', 'C']}
print(f'Создали film:\n{route.create_film(film=film)}\n')

print(f'Удаление film по id:\n{route.delete_film(film_id=1)}\n')

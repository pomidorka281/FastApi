from fastapi.testclient import TestClient
from route import app

client = TestClient(app)


def test_create_film():
    film_data = {"name": "string", "year": 2024, "rating": 10,
                "tags":['A', 'B', 'C']}
    response = client.post("/film/", json=film_data)
    assert response.status_code == 200
    assert response.json()["name"] == film_data["name"]


def test_get_films():
    year = 2024
    tag1 = "A"
    tag2 = "B"
    tag3 = "C"
    response = client.get(f"/film/?year={year}&tag={tag1}&tag={tag2}&tag={tag3}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_film():
    film_id = 1
    response = client.get(f"/film/{film_id}")
    assert response.status_code == 200
    assert response.json()[0]["id"] == film_id


def test_update_film():
    film_id = 1
    film = {"name": "qwer", "year": 2023, "rating": 8.9, "tags":['3', '2', 'r']}
    response = client.put(f"/film/{film_id}", json=film)
    assert response.status_code == 200


def test_delete_film():
    film_id = 1
    response = client.delete(f"/film/{film_id}")
    assert response.status_code == 200
    assert response.json()[0]["id"] == film_id


print(test_create_film())
print(test_get_films())
print(test_get_film())
print(test_update_film())
print(test_delete_film())

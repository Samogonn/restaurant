from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_menu():
    response = client.get("/menu/3")
    assert response.status_code == 200
    assert response.json() == {
        "name": "Papa's Burgers",
        "description": "Family restaurant",
        "id": 3,
    }


def test_get_inexistent_menu():
    response = client.get("/menu/99")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}


def test_create_menu():
    menu = {"description": "Never spicy taco", "name": "Dragon's Tacos"}
    response = client.post("/menu", params=menu)
    assert response.status_code == 201


def test_get_all_menus():
    response = client.get("/menu")
    assert response.status_code == 200
    assert response.json() == [
        {"description": "Delicious pizza!", "id": 2, "name": "Best Pizza"},
        {
            "description": "Family restaurant",
            "id": 3,
            "name": "Papa's Burgers",
        },
        {"description": "Never spicy taco", "id": 4, "name": "Dragon's Tacos"},
    ]


def test_update_menu():
    id = 4
    menu = {
        "description": "Always spicy taco",
        "name": "Not for Dragon's Tacos",
    }
    response = client.patch(f"/menu/{id}", params=menu)
    assert response.status_code == 200
    assert response.json() == {
        "description": "Always spicy taco",
        "id": 4,
        "name": "Not for Dragon's Tacos",
    }

    response = client.get("/menu")
    assert response.json() == [
        {"description": "Delicious pizza!", "id": 2, "name": "Best Pizza"},
        {
            "description": "Family restaurant",
            "id": 3,
            "name": "Papa's Burgers",
        },
        {
            "description": "Always spicy taco",
            "id": 4,
            "name": "Not for Dragon's Tacos",
        },
    ]


def test_remove_menu():
    id = 4
    response = client.delete(f"/menu/{id}")
    assert response.status_code == 200
    assert response.json() == {
        "description": "Always spicy taco",
        "id": 4,
        "name": "Not for Dragon's Tacos",
    }

    response = client.get("/menu")
    assert response.json() == [
        {"description": "Delicious pizza!", "id": 2, "name": "Best Pizza"},
        {
            "description": "Family restaurant",
            "id": 3,
            "name": "Papa's Burgers",
        },
    ]


def test_remove_inexistent_menu():
    id = 4
    response = client.delete(f"/menu/{id}")
    assert response.status_code == 404

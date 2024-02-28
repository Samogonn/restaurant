from fastapi.testclient import TestClient


def test_get_menu(client: TestClient):
    response = client.get("/menu/1")
    assert response.status_code == 200
    assert response.json() == {
        "description": "Delicious pizza!",
        "id": 1,
        "name": "Best Pizza",
    }


def test_get_inexistent_menu(client: TestClient):
    response = client.get("/menu/99")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}


def test_get_all_menus(client: TestClient):
    response = client.get("/menu")
    assert response.status_code == 200
    assert response.json() == [
        {"description": "Delicious pizza!", "id": 1, "name": "Best Pizza"},
        {
            "description": "Family restaurant",
            "id": 2,
            "name": "Papa's Burgers",
        },
    ]


def test_create_menu(client: TestClient):
    menu = {"description": "Never spicy taco", "name": "Dragon Tacos"}
    response = client.post("/menu", params=menu)
    assert response.status_code == 201
    assert response.json() == {
        "description": "Never spicy taco",
        "id": 3,
        "name": "Dragon Tacos",
    }


def test_update_menu(client: TestClient):
    id = 3
    menu = {
        "description": "Always spicy taco",
        "name": "Not for Dragon Tacos",
    }
    response = client.patch(f"/menu/{id}", params=menu)
    assert response.status_code == 200
    assert response.json() == {
        "description": "Always spicy taco",
        "id": 3,
        "name": "Not for Dragon Tacos",
    }

    response = client.get("/menu")
    assert response.json() == [
        {"description": "Delicious pizza!", "id": 1, "name": "Best Pizza"},
        {
            "description": "Family restaurant",
            "id": 2,
            "name": "Papa's Burgers",
        },
        {
            "description": "Always spicy taco",
            "id": 3,
            "name": "Not for Dragon Tacos",
        },
    ]


def test_remove_menu(client: TestClient):
    id = 3
    response = client.delete(f"/menu/{id}")
    assert response.status_code == 200
    assert response.json() == {
        "description": "Always spicy taco",
        "id": 3,
        "name": "Not for Dragon Tacos",
    }

    response = client.get("/menu")
    assert response.json() == [
        {"description": "Delicious pizza!", "id": 1, "name": "Best Pizza"},
        {
            "description": "Family restaurant",
            "id": 2,
            "name": "Papa's Burgers",
        },
    ]


def test_remove_inexistent_menu(client: TestClient):
    id = 4
    response = client.delete(f"/menu/{id}")
    assert response.status_code == 404

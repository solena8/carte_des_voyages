def test_create_place(client):
    place_data = {
        "name": "Test SchemaPlace",
        "date": "2025-02-06T12:00:00",
        "city": "Test City",
        "country": "Test Country",
        "latitude": 48.8566,
        "longitude": 2.3522
    }
    response = client.post("/places/", json=place_data)
    assert response.status_code == 200
    assert response.json()["name"] == place_data["name"]
    assert response.json()["date"] == place_data["date"]
    assert response.json()["city"] == place_data["city"]
    assert response.json()["country"] == place_data["country"]
    assert response.json()["latitude"] == place_data["latitude"]
    assert response.json()["longitude"] == place_data["longitude"]


def test_get_places(client):
    response = client.get("/places/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

from app.models.model_places import ModelPlace

def test_place_model():
    place = ModelPlace(
        name="Test Place",
        city="Test City",
        country="Test Country",
        latitude=48.8566,
        longitude=2.3522
    )
    assert place.name == "Test Place"
    assert place.city == "Test City"
    assert place.country == "Test Country"
    assert place.latitude == 48.8566
    assert place.longitude == 2.3522


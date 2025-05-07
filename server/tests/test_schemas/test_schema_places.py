import pytest
from datetime import datetime
from app.schemas.schema_places import SchemaPlaceCreate
from pydantic import ValidationError

def test_valid_place_creation():
    valid_data = {
        "name": "Test Place",
        "date": "2025-02-06T12:00:00",
        "city": "Test City",
        "country": "Test Country",
        "latitude": 48.8566,
        "longitude": 2.3522
    }
    place = SchemaPlaceCreate(**valid_data)
    assert isinstance(place.date, datetime)
    assert place.name == valid_data["name"]

def test_missing_required_fields():
    invalid_data = {
        "name": "Test SchemaPlace"
    }
    with pytest.raises(ValidationError):
        SchemaPlaceCreate(**invalid_data)

def test_invalid_date_format():
    invalid_data = {
        "name": "Test SchemaPlace",
        "date": "invalid-date",
        "city": "Test City",
        "country": "Test Country",
        "latitude": 48.8566,
        "longitude": 2.3522
    }
    with pytest.raises(ValidationError):
        SchemaPlaceCreate(**invalid_data)

def test_invalid_coordinates():
    invalid_data = {
        "name": "Test SchemaPlace",
        "date": "2025-02-06T12:00:00",
        "city": "Test City",
        "country": "Test Country",
        "latitude": "not-a-number",
        "longitude": 2.3522
    }
    with pytest.raises(ValidationError):
        SchemaPlaceCreate(**invalid_data)

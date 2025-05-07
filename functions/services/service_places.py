from sqlalchemy.orm import Session
from functions.models.model_places import ModelPlace
from functions.schemas.schema_places import SchemaPlaceCreate

def create_new_place(db: Session, place: SchemaPlaceCreate):
    db_place = ModelPlace(
        name=place.name,
        date=place.date,
        city=place.city,
        country=place.country,
        latitude=place.latitude,
        longitude=place.longitude,
        image=place.image
    )
    db.add(db_place)
    db.commit()
    db.refresh(db_place)
    return db_place

from fastapi import APIRouter
from sqlalchemy.orm import Session
from functions.services.service_places import create_new_place
from functions.schemas import schema_places as schemas
from functions.dependencies import get_db
from functions.models.model_places import ModelPlace
from fastapi import Depends, status, HTTPException

router = APIRouter()  # permet de structurer le projet en plusieurs fichiers et séparer les fonctionnalités :


@router.post("/", response_model=schemas.SchemaPlaceCreate)
def create_place(place: schemas.SchemaPlaceCreate, db: Session = Depends(get_db)):
    return create_new_place(db=db, place=place)


@router.get("/", response_model=list[schemas.SchemaPlace])
async def read_places(db: Session = Depends(get_db)):
    return db.query(ModelPlace).all()


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_place(id: int, db: Session = Depends(get_db)):
    place = db.query(ModelPlace).filter(ModelPlace.id == id).first()
    if place is None:
        raise HTTPException(status_code=404, detail="SchemaPlace not found")
    db.delete(place)
    db.commit()
    return {"message": "SchemaPlace deleted successfully"}


@router.get("/api/stats")
def get_stats(db: Session = Depends(get_db)):
    total_entries = db.query(ModelPlace).count()
    unique_countries = db.query(ModelPlace.country).distinct().count()
    return {"totalEntries": total_entries, "uniqueCountries": unique_countries}

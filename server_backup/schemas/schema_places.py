from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class Config:
    from_attributes = True #configuration pour convertir automatiquement les attributs
    # d'objets ou d'instances de classes en modèles Pydantic.

# pydantic = ces classes permettent un controle automatique
# de la structure des données dans routes-places en agument des méthodes
# ( ex : @router.post("/", response_model=schemas.SchemaPlaceCreate)

# les deux classes servent de dto

# pour les données sortantes de la db
class SchemaPlace(BaseModel):
    id: int = None
    name: str
    date: datetime = None
    city: str
    country: str
    latitude: float
    longitude: float
    image: Optional[bytes] = None

#pour les données entrantes dans la db
class SchemaPlaceCreate(BaseModel):
    name: str
    date: datetime
    city: str
    country: str
    latitude: float
    longitude: float
    image: Optional[bytes] = None


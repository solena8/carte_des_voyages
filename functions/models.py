from typing import List

from pydantic import RootModel
from firedantic import Model
from datetime import datetime


class Place(Model):
    __collection__ = "places"
    # id: str
    name: str
    date: datetime
    city: str
    country: str
    latitude: float
    longitude: float
    # image = Column(LargeBinary)


class PlaceList(RootModel):
    root: List[Place]


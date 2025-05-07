from sqlalchemy import Column, Integer, String, DateTime, Float, LargeBinary
from datetime import datetime
from functions.database import Base


class ModelPlace(Base):
    __tablename__ = "places"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    date = Column(DateTime, default=datetime)
    city = Column(String, index=True)
    country = Column(String, index=True)
    latitude = Column(Float, index=True)
    longitude = Column(Float, index=True)
    image = Column(LargeBinary)



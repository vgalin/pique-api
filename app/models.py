from sqlalchemy import Column, Integer, String

from geoalchemy2 import Geometry
from .database import Base


class Peak(Base):
    __tablename__ = 'peak'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    geom = Column(Geometry('POINT'))
